package main

import (
	"os"

	"github.com/bbengfort/rvasp"
	"github.com/urfave/cli"
)

func main() {
	app := cli.NewApp()

	app.Name = "rvasp"
	app.Version = rvasp.Version()
	app.Usage = "a gRPC based directory service for TRISA identity lookups"
	app.Flags = []cli.Flag{}
	app.Commands = []cli.Command{
		{
			Name:     "serve",
			Usage:    "run the rVASP service",
			Category: "server",
			Action:   serve,
			Flags: []cli.Flag{
				cli.StringFlag{
					Name:  "a, addr",
					Usage: "the address and port to bind the server on",
					Value: ":4434",
				},
				cli.StringFlag{
					Name:  "d, db",
					Usage: "the dsn to the sqlite3 database to connect to",
					Value: "fixtures/rvasp.db",
				},
			},
		},
	}

	app.Run(os.Args)
}

// Serve the TRISA directory service
func serve(c *cli.Context) (err error) {
	var srv *rvasp.Server
	if srv, err = rvasp.New(c.String("db")); err != nil {
		return cli.NewExitError(err, 1)
	}

	if err = srv.Serve(c.String("addr")); err != nil {
		return cli.NewExitError(err, 1)
	}
	return nil
}
