#!/usr/bin/env python

import pigpio

class tx:

   """
   """

   def __init__(self, pi, gpio, carrier_hz):

      """
      Initialises an IR tx on a Pi's gpio with a carrier of
      carrier_hz.

      http://www.hifi-remote.com/infrared/IR-PWM.shtml
      """

      self.pi = pi
      self.gpio = gpio
      self.carrier_hz = carrier_hz
      self.micros = 1000000 / carrier_hz  # Convert carrier freq into micro seconds, ie. carrier of 38khz -> micros = 26.3
      self.on_mics = self.micros / 2      # Duty cycle
      self.off_mics = self.micros - self.on_mics
      self.offset = 0

      self.wf = []
      self.wid = -1

      pi.set_mode(gpio, pigpio.OUTPUT)

   def clear_code(self):
      self.wf = []
      if self.wid >= 0:
         self.pi.wave_delete(self.wid)
         self.wid = -1

   def construct_code(self):
      if len(self.wf) > 0:
         pulses = self.pi.wave_add_generic(self.wf)
         print("waveform TOTAL {} pulses".format(pulses))
         self.wid = self.pi.wave_create()

   def send_code(self):
      if self.wid >= 0:
         self.pi.wave_send_once(self.wid)
         while self.pi.wave_tx_busy():
            pass

   def add_to_code(self, on, off):

      # is there room for more pulses?

      if (on*2) + 1 + len(self.wf) > 680: # 682 is maximum
         
         pulses = self.pi.wave_add_generic(self.wf)
         print("waveform partial {} pulses".format(pulses))
         self.offset = self.pi.wave_get_micros()

         # continue pulses from offset
         self.wf = [pigpio.pulse(0, 0, self.offset)]

      # add on cycles of carrier
      for x in range(on):
         self.wf.append(pigpio.pulse(1<<self.gpio, 0, self.on_mics))
         self.wf.append(pigpio.pulse(0, 1<<self.gpio, self.off_mics))

      # add off cycles of no carrier
      self.wf.append(pigpio.pulse(0, 0, off * self.micros))

if __name__ == "__main__":

   import time
   import pigpio
   import ir_tx

   pi = pigpio.pi()

   # tx(pi, gpio, frequency)
   tx = ir_tx.tx(pi, 25, 38000)

   for x in range(1024):
      tx.clear_code()

      tx.add_to_code(96, 24) # lead-in burst code

      for b in range(10):

         if x & (1<<b): # 1 bit
            tx.add_to_code(48, 24) # 1 burst-code
         else:
            tx.add_to_code(24, 24) # 0 burst-code

      tx.add_to_code(24, 1024) # lead-out burst code

      tx.construct_code()

      tx.send_code()

   tx.clear_code()

   pi.stop()

