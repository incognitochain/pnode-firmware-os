package golang

import (
	"encoding/json"
	"log"
	"time"

	brain "github.com/duyhtq/brain/master"
	"github.com/duyhtq/maya/brain/ports"
	zmq "github.com/pebbe/zmq4"
)

func SendTo(channel, message string) {
	socket, e := zmq.NewSocket(zmq.PUSH)
	if e != nil {
		log.Println("Fail to create socket:", e)
	}
	// keep socket alive a little longer to avoid lost messages.
	defer time.Sleep(time.Second)
	defer socket.Close()

	if e := socket.Connect(channel); e != nil {
		log.Println("Fail to connect to ", channel, ". Error:", e)
	}

	if _, e := socket.Send(message, 0); e != nil {
		log.Println("Fail to send via zmq:", e)
	}

}

func SendJson(json string) {
	socket, e := zmq.NewSocket(zmq.PUSH)
	if e != nil {
		log.Println("Fail to create socket:", e)
	}
	// keep socket alive a little longer to avoid lost messages.
	//defer time.Sleep(time.Second)
	defer socket.Close()

	if e := socket.Connect(ports.SENSORS); e != nil {
		log.Fatal("Fail to connect to channel", ports.SENSORS, e)
	}

	if _, e := socket.Send(json, 0); e != nil {
		log.Println("Fail to send via zmq:", e)
	}
}

func SendSensor(s brain.Sensor) {
	socket, e := zmq.NewSocket(zmq.PUSH)
	if e != nil {
		log.Println("Fail to create socket:", e)
	}
	// keep socket alive a little longer to avoid lost messages.
	defer time.Sleep(time.Second)
	defer socket.Close()

	if e := socket.Connect(ports.SENSORS); e != nil {
		log.Fatal("Fail to connect to channel", ports.SENSORS, e)
	}
	if b, e := json.Marshal(s); e != nil {
		log.Println("Can't marshal object", s, ". Error:", e)
	} else if _, e := socket.SendBytes(b, 0); e != nil {
		log.Println("Fail to send via zmq:", e)
	}
}
