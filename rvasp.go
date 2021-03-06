package rvasp

import (
	"context"
	"errors"
	"fmt"
	"io"
	"math/rand"
	"net"
	"os"
	"os/signal"
	"time"

	"github.com/bbengfort/rvasp/pb"
	log "github.com/sirupsen/logrus"
	"google.golang.org/grpc"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

// New creates a rVASP server with the specified configuration and prepares
// it to listen for and serve GRPC requests.
func New(dsn string) (s *Server, err error) {
	s = &Server{}
	if s.db, err = gorm.Open(sqlite.Open(dsn), &gorm.Config{}); err != nil {
		return nil, err
	}

	if err = MigrateDB(s.db); err != nil {
		return nil, err
	}

	// TODO: mark the VASP local based on name or configuration rather than erroring
	if err = s.db.Where("is_local = ?", true).First(&s.vasp).Error; err != nil {
		return nil, fmt.Errorf("could not fetch local VASP info from database: %s", err)
	}

	return s, nil
}

// Server implements the GRPC TRISAInterVASP and TRISADemo services.
type Server struct {
	srv  *grpc.Server
	db   *gorm.DB
	vasp VASP
}

// Serve GRPC requests on the specified address.
func (s *Server) Serve(addr string) (err error) {
	// Initialize the gRPC server
	s.srv = grpc.NewServer()
	pb.RegisterTRISADemoServer(s.srv, s)
	pb.RegisterTRISAIntegrationServer(s.srv, s)

	// Catch OS signals for graceful shutdowns
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt)
	go func() {
		<-quit
		s.Shutdown()
	}()

	// Listen for TCP requests on the specified address and port
	var sock net.Listener
	if sock, err = net.Listen("tcp", addr); err != nil {
		return fmt.Errorf("could not listen on %q", addr)
	}
	defer sock.Close()

	// Run the server
	log.Infof("listening on %s", addr)
	return s.srv.Serve(sock)
}

// Shutdown the TRISA Directory Service gracefully
func (s *Server) Shutdown() (err error) {
	log.Info("gracefully shutting down")
	s.srv.GracefulStop()
	return nil
}

// Transfer accepts a transfer request from a beneficiary and begins the InterVASP
// protocol to perform identity verification prior to establishing the transactoin in
// the blockchain between crypto wallet addresses.
func (s *Server) Transfer(ctx context.Context, req *pb.TransferRequest) (rep *pb.TransferReply, err error) {
	return nil, nil
}

// AccountStatus is a demo RPC to allow demo clients to fetch their recent transactions.
func (s *Server) AccountStatus(ctx context.Context, req *pb.AccountRequest) (rep *pb.AccountReply, err error) {
	rep = &pb.AccountReply{}

	// Lookup the account in the database
	var account Account
	if err = LookupAccount(s.db, req.Account).First(&account).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			rep.Error = pb.Errorf(pb.ErrNotFound, "account not found")
			log.Info(rep.Error.Error())
			return rep, nil
		}
		log.Error(err.Error())
		return nil, err
	}

	rep.Name = account.Name
	rep.Email = account.Email
	rep.WalletAddress = account.WalletAddress
	rep.Balance = account.BalanceFloat()
	rep.Completed = account.Completed
	rep.Pending = account.Pending

	if !req.NoTransactions {
		var transactions []Transaction
		if transactions, err = account.Transactions(s.db); err != nil {
			log.Error(err.Error())
			return nil, err
		}

		rep.Transactions = make([]*pb.Transaction, 0, len(transactions))
		for _, transaction := range transactions {
			rep.Transactions = append(rep.Transactions, &pb.Transaction{
				Account: transaction.Account.Email,
				Originator: &pb.Identity{
					WalletAddress: transaction.Originator.WalletAddress,
					Email:         transaction.Originator.Wallet.Email,
					Ivms101:       transaction.Originator.IVMS101,
					Provider:      transaction.Originator.Provider,
				},
				Beneficiary: &pb.Identity{
					WalletAddress: transaction.Beneficiary.WalletAddress,
					Email:         transaction.Beneficiary.Wallet.Email,
					Ivms101:       transaction.Beneficiary.IVMS101,
					Provider:      transaction.Beneficiary.Provider,
				},
				Amount:    transaction.AmountFloat(),
				Debit:     transaction.Debit,
				Completed: transaction.Completed,
				Timestamp: transaction.Timestamp.Format(time.RFC3339),
			})
		}
	}

	log.Infof("account status %s with %d transactions", rep.Email, len(rep.Transactions))
	return rep, nil
}

// LiveUpdates is a demo bidirectional RPC that allows demo clients to explicitly show
// the message interchange between VASPs during the InterVASP protocol. The demo client
// connects to both sides of a transaction and can push commands to the stream; any
// messages received by the VASP as they perform the protocol are sent down to the UI.
func (s *Server) LiveUpdates(stream pb.TRISADemo_LiveUpdatesServer) (err error) {
	var (
		client   string
		messages uint64
	)

	for {
		var req *pb.Command
		if req, err = stream.Recv(); err != nil {
			// The stream was closed on the client side
			if err == io.EOF {
				if client == "" {
					log.Warn("live updates connection closed before first message")
				} else {
					log.Warnf("live updates connection from client %s closed", client)
				}
			}

			// Some other error occurred
			log.Errorf("connection from client %q dropped: %s", client, err)
			return nil
		}

		// If this is the first time we've seen the client, log it
		if client == "" {
			client = req.Client
			log.Infof("client %s connected to live updates", client)
		} else if client != req.Client {
			log.Warnf("received message from %q but expected it from %q", req.Client, client)
		}

		// Handle the message
		messages++
		log.Infof("received message %d: %s", messages, req)

		switch req.Type {
		case pb.RPC_NORPC:
			// Send back an acknowledgement message
			ack := &pb.Message{
				Type:      pb.RPC_NORPC,
				Id:        req.Id,
				Update:    fmt.Sprintf("command %d acknowledged", req.Id),
				Timestamp: time.Now().Format(time.RFC3339),
			}
			if err = stream.Send(ack); err != nil {
				log.Errorf("could not send message to %q: %s", client, err)
				return err
			}
		case pb.RPC_ACCOUNT:
			var rep *pb.AccountReply
			if rep, err = s.AccountStatus(context.Background(), req.GetAccount()); err != nil {
				return err
			}

			ack := &pb.Message{
				Type:      pb.RPC_ACCOUNT,
				Id:        req.Id,
				Timestamp: time.Now().Format(time.RFC3339),
				Reply:     &pb.Message_Account{Account: rep},
			}

			if err = stream.Send(ack); err != nil {
				log.Errorf("could not send message to %q: %s", client, err)
				return err
			}
		case pb.RPC_TRANSFER:
			// HACK: simulate the TRISA process as a quick stub to unblock the front end
			if err = s.simulateTRISA(stream, req, client); err != nil {
				log.Error(err.Error())
				return err
			}
		}
	}
}

func (s *Server) simulateTRISA(stream pb.TRISADemo_LiveUpdatesServer, req *pb.Command, client string) (err error) {
	// Create stream updater context for sending live updates back to client
	updater := newStreamUpdater(stream, req, client)

	// Get the transfer from the original command, will panic if nil
	transfer := req.GetTransfer()

	// Lookup the account associated with the transfer originator
	var account Account
	if err = LookupAccount(s.db, transfer.Account).First(&account).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			rep := &pb.Message{
				Type:      pb.RPC_TRANSFER,
				Id:        req.Id,
				Timestamp: time.Now().Format(time.RFC3339),
				Category:  pb.MessageCategory_ERROR,
				Reply: &pb.Message_Transfer{Transfer: &pb.TransferReply{
					Error: pb.Errorf(pb.ErrNotFound, "account not found"),
				}},
			}

			if err = stream.Send(rep); err != nil {
				return fmt.Errorf("could not send transfer reply to %q: %s", client, err)
			}
			return nil
		}
		return fmt.Errorf("could not fetch account: %s", err)
	}
	if err = updater.send(fmt.Sprintf("account %d accessed successfully", account.ID), pb.MessageCategory_LEDGER); err != nil {
		return err
	}

	// Lookup the wallet of the beneficiary
	var beneficiary Wallet
	if err = LookupBeneficiary(s.db, transfer.Beneficiary).First(&beneficiary).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			rep := &pb.Message{
				Type:      pb.RPC_TRANSFER,
				Id:        req.Id,
				Timestamp: time.Now().Format(time.RFC3339),
				Category:  pb.MessageCategory_ERROR,
				Reply: &pb.Message_Transfer{Transfer: &pb.TransferReply{
					Error: pb.Errorf(pb.ErrNotFound, "beneficiary wallet not found"),
				}},
			}

			if err = stream.Send(rep); err != nil {
				return fmt.Errorf("could not send transfer reply to %q: %s", client, err)
			}
			return nil
		}
		return fmt.Errorf("could not fetch beneficiary wallet: %s", err)
	}
	if err = updater.send(fmt.Sprintf("wallet %s (%s) provided by %s", beneficiary.Address, beneficiary.Email, beneficiary.Provider.Name), pb.MessageCategory_BLOCKCHAIN); err != nil {
		return err
	}

	if err = updater.send("beginning TRISA protocol for identity exchange", pb.MessageCategory_TRISAP2P); err != nil {
		return err
	}

	if err = updater.send("VASP public key not cached, looking up TRISA directory service", pb.MessageCategory_TRISADS); err != nil {
		return err
	}

	time.Sleep(time.Duration(rand.Int63n(1800)) * time.Millisecond)
	if err = updater.send("sending handshake request to [endpoint]", pb.MessageCategory_TRISAP2P); err != nil {
		return err
	}

	time.Sleep(time.Duration(rand.Int63n(2200)) * time.Millisecond)
	if err = updater.send("[vasp] verified, secure TRISA connection established", pb.MessageCategory_TRISAP2P); err != nil {
		return err
	}

	time.Sleep(time.Duration(rand.Int63n(1800)) * time.Millisecond)
	if err = updater.send(fmt.Sprintf("identity for beneficiary %q confirmed - beginning transaction", beneficiary.Email), pb.MessageCategory_BLOCKCHAIN); err != nil {
		return err
	}

	time.Sleep(time.Duration(rand.Int63n(6200)) * time.Millisecond)
	if err = updater.send("transaction appended to blockchain, sending hash to [endpoint]", pb.MessageCategory_BLOCKCHAIN); err != nil {
		return err
	}

	time.Sleep(time.Duration(rand.Int63n(1000)) * time.Millisecond)
	rep := &pb.Message{
		Type:      pb.RPC_TRANSFER,
		Id:        req.Id,
		Timestamp: time.Now().Format(time.RFC3339),
		Category:  pb.MessageCategory_LEDGER,
		Reply: &pb.Message_Transfer{Transfer: &pb.TransferReply{
			Transaction: &pb.Transaction{
				Account: account.Email,
				Originator: &pb.Identity{
					WalletAddress: account.WalletAddress,
					Email:         account.Email,
					Ivms101:       account.IVMS101,
					Provider:      s.vasp.IVMS101,
				},
				Beneficiary: &pb.Identity{
					WalletAddress: beneficiary.Address,
					Email:         beneficiary.Email,
					Ivms101:       "[simulated]",
					Provider:      "[simulated]",
				},
				Amount:    transfer.Amount,
				Debit:     true,
				Completed: true,
				Timestamp: time.Now().Format(time.RFC3339),
			},
		}},
	}

	if err = stream.Send(rep); err != nil {
		return fmt.Errorf("could not send transfer reply to %q: %s", client, err)
	}

	return nil
}

// create a stream updater for simulating live update messages
func newStreamUpdater(stream pb.TRISADemo_LiveUpdatesServer, req *pb.Command, client string) *streamUpdater {
	return &streamUpdater{
		stream:    stream,
		client:    client,
		requestID: req.Id,
	}
}

// streamUpdater holds the context for sending updates based on a single request.
type streamUpdater struct {
	stream    pb.TRISADemo_LiveUpdatesServer
	client    string
	requestID uint64
}

func (s *streamUpdater) send(update string, cat pb.MessageCategory) (err error) {
	msg := &pb.Message{
		Type:      pb.RPC_NORPC,
		Id:        s.requestID,
		Update:    update,
		Category:  cat,
		Timestamp: time.Now().Format(time.RFC3339),
	}

	if err = s.stream.Send(msg); err != nil {
		return fmt.Errorf("could not send message to %q: %s", s.client, err)
	}
	return nil
}
