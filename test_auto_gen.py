#!/usr/bin/python2
import os
import unittest
from jumper.vlab import Vlab

class TestClass(unittest.TestCase):
    _is_pass = False
    _condition_found = False
    _PASS = "Pass"
    _FAIL = "Fail"
    args = {}


    def setUp(self):
        ##################
        # change these arguments
        #################
        self.args['filename'] = 'BUILD/STM32_Button_Debounce.bin' # your firmware file here
        self.args['timeout'] = 5000         # default of 10s. Set your timeout for the test   
        self.args['timeout_result'] = self._PASS # or self._FAIL
        self.args['uart_test'] = True            # should look for uart value?
        self.args['uart_test_value'] = 'mBed boot done'
        self.args['uart_test_result'] = self._PASS # or self._FAIL
        self.args['gpio_test'] = False   # should look for GPIO value?
        self.args['gpio_test_pin'] = 17 # or any other pin number
        self.args['gpio_test_value'] = 0 # or 1
        self.args['gpio_test_result'] = self._PASS # or self._FAIL

        # set up the device simulation
        self.v = Vlab(working_directory=".", print_uart=True, token="demo-token-for-ci")
        self.v.load(self.args['filename'])
        self.v.on_pin_level_event(self.pin_listener)
        self.v.on_uart_read_line(self.on_uart_read_line)
        # running for a while to get the BSP done
        self.is_led_on = False
        self.times_pressed = 0
        self.v.run_for_ms(10)

    def tearDown(self):
        self.v.stop()

    def pin_listener(self, pin_number, pin_level):
        if self.args['gpio_test'] and self.args['gpio_test_pin'] == pin_number and self.args['gpio_test_value'] == pin_level:
            self._is_pass = True if self.args['gpio_test_result'] == self._PASS else False
            self._condition_found = True

    def on_uart_read_line(self, uart_print):
        if self.args['uart_test'] and str(self.args['uart_test_value']) in uart_print:
            self._is_pass = True if self.args['uart_test_result'] == self._PASS else False
            self._condition_found = True
    
    def test_debouncer(self):
        self.v.run_for_ms(self.args['timeout'])

        if self._condition_found:
            self.assertEqual(self._is_pass, True)
        else:
            self.assertEqual(self.args['timeout_result'], self._PASS)

if __name__ == '__main__':
    unittest.main()
