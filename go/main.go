package main

// #cgo LDFLAGS: -L${SRCDIR}/ -ldisplayconfig
// #include <windows.h>
// #include <stdio.h>
// #include <stdlib.h>
// #include <string.h>
// void clone_extend();
// void set_resolution(const unsigned int *width, const unsigned int *height);
import "C"

import (
	"errors"
	"log"
	"os"
	"strings"

	"github.com/getlantern/systray"
	"github.com/gordonklaus/portaudio"
	"golang.org/x/sys/windows/registry"
)

type sound struct {
	*portaudio.Stream
	buffer []float32
	i      int
}

var isSoundOn bool = false

func handleChangeDpi(dpi uint8) {
	realValue := 0
	if dpi == 125 {
		realValue = 1
	}
	key := "Control Panel\\Desktop\\PerMonitorSettings\\AUS2722L5LMQS083030_14_07E4_8C^A133EEACD46DEB102F26E14D876CFD94"
	log.Println("Opening key")
	handle, err := registry.OpenKey(registry.CURRENT_USER, key, registry.SET_VALUE)
	chk(err)
	log.Printf("Setting value to %d", realValue)
	err = handle.SetDWordValue("DpiValue", uint32(realValue))
	chk(err)
	log.Println("Closing key")
	err = handle.Close()
	chk(err)
}

func handleChangeResolution(mButton *systray.MenuItem, width C.uint, height C.uint, dpi uint8) {
	for {
		<-mButton.ClickedCh
		handleChangeDpi(dpi)
		log.Printf("Changing resolution to %d %d", width, height)
		C.set_resolution(&width, &height)
	}
}

func handleQuit(mQuit *systray.MenuItem) {
	<-mQuit.ClickedCh // Wait for the "Quit" item to be clicked
	systray.Quit()    // Quit the application
}

func mHandleCloneExtend(mCloneExtend *systray.MenuItem) {
	for {
		<-mCloneExtend.ClickedCh
		C.clone_extend()
	}
}

func mHandleSound(mSound *systray.MenuItem, stream *sound) {
	for {
		<-mSound.ClickedCh
		if !isSoundOn {
			chk(stream.Start())
			isSoundOn = true
			mSound.Check()
		} else {
			chk(stream.Stop())
			isSoundOn = false
			mSound.Uncheck()
		}
	}
}

func main() {
	systray.Run(onReady, onExit)
	log.Println("Opened app")
}

func onReady() {
	b, err := os.ReadFile("../peepo.ico")
	chk(err)
	systray.SetIcon(b)
	systray.SetTitle("Resolution Changer")

	mQHD := systray.AddMenuItem("1440p", "")
	go handleChangeResolution(mQHD, C.uint(2560), C.uint(1440), 125)
	mFHD := systray.AddMenuItem("1080p", "")
	go handleChangeResolution(mFHD, C.uint(1920), C.uint(1080), 100)
	mValo := systray.AddMenuItem("Valo res", "")
	go handleChangeResolution(mValo, C.uint(1280), C.uint(880), 100)
	mSound := systray.AddMenuItemCheckbox("PS5 sound", "", isSoundOn)

	go func() {
		portaudio.Initialize()
		defer portaudio.Terminate()

		sound, err := initStream()

		if err != nil {
			mSound.Disable()
			return
		}
		defer sound.Close()
		mHandleSound(mSound, sound)
	}()

	mCloneExtend := systray.AddMenuItem("Clone/Extend", "")
	go mHandleCloneExtend(mCloneExtend)

	mQuit := systray.AddMenuItem("Quit", "")
	go handleQuit(mQuit)
}

func onExit() {
	systray.Quit()
}

func chk(err error) {
	if err != nil {
		panic(err)
	}
}

func initStream() (*sound, error) {
	devices, err := portaudio.Devices()
	chk(err)
	for _, device := range devices {
		if device.HostApi.Name == "Windows WASAPI" &&
			strings.Contains(device.Name, "CODEC") &&
			strings.Contains(device.Name, "PS5") {
			p := portaudio.LowLatencyParameters(device, device.HostApi.DefaultOutputDevice)
			p.Input.Channels = 1
			p.Output.Channels = 1

			log.Println(device.HostApi.Name)
			log.Println(device.Name)
			log.Println(device.HostApi.DefaultOutputDevice.Name)

			e := &sound{buffer: make([]float32, int(p.SampleRate))}
			e.Stream, err = portaudio.OpenStream(p, e.processAudio)
			chk(err)
			log.Println(e.Info().SampleRate)
			return e, nil
		}
	}
	return &sound{}, errors.New("device was not found")
}

func (e *sound) processAudio(in, out []float32) {
	for i := range out {
		out[i] = in[i]
	}
}
