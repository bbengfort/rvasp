package rvasp

import (
	"context"
	"errors"
	"fmt"
	"io"
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

	return s, nil
}

// Server implements the GRPC TRISAInterVASP and TRISADemo services.
type Server struct {
	srv *grpc.Server
	db  *gorm.DB
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
	if err = s.db.Where("email = ?", req.Account).First(&account).Error; err != nil {
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
		}
	}
}
