package rvasp

import (
	"context"
	"fmt"
	"net"
	"os"
	"os/signal"

	"github.com/bbengfort/rvasp/pb"
	log "github.com/sirupsen/logrus"
	"google.golang.org/grpc"
)

// New creates a rVASP server with the specified configuration and prepares
// it to listen for and serve GRPC requests.
func New() (s *Server, err error) {
	s = &Server{}
	return s, nil
}

// Server implements the GRPC TRISAInterVASP and TRISADemo services.
type Server struct {
	srv *grpc.Server
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

// TransferTo accepts a transfer request from a beneficiary and begins the InterVASP
// protocol to perform identity verification prior to establishing the transactoin in
// the blockchain between crypto wallet addresses.
func (s *Server) TransferTo(ctx context.Context, req *pb.TransferRequest) (rep *pb.TransferReply, err error) {
	return nil, nil
}

// AccountStatus is a demo RPC to allow demo clients to fetch their recent transactions.
func (s *Server) AccountStatus(ctx context.Context, req *pb.AccountRequest) (rep *pb.AccountReply, err error) {
	return nil, nil
}

// LiveUpdates is a demo bidirectional RPC that allows demo clients to explicitly show
// the message interchange between VASPs during the InterVASP protocol. The demo client
// connects to both sides of a transaction and can push commands to the stream; any
// messages received by the VASP as they perform the protocol are sent down to the UI.
func (s *Server) LiveUpdates(stream pb.TRISADemo_LiveUpdatesServer) error {
	return nil
}
