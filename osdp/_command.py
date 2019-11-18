from abc import ABC, abstractmethod

from ._types import *
from ._message import Message
from ._device import Device

class Command(Message):

	def __init__(self):
		self._address = None
		self._code = None

	@property
	@abstractmethod
	def command_code(self) -> int:
		pass

	@abstractmethod
	def security_control_block(self) -> bytes:
		pass

	@abstractmethod
	def custom_command_update(self, command_buffer: bytearray):
		pass

	def build_command(self, device: Device) -> bytes:
		command_buffer = bytearray([
			self.SOM,
			self.address,
			0x00,
			0x00,
			device.message_control.control_byte
		])

		if device.message_control.has_security_control_block:
			command_buffer.extend(self.security_control_block())

		command_buffer.append(self.command_code)

		if device.is_security_established:
			command_buffer.extend(self.encrypted_data(device))

			# TODO: I don't think this needed
			# include mac and crc/checksum in length before generating mac
			# additional_length = 4 + (device.message_control.use_crc ? 2 : 1)
			# self.add_packet_length(command_buffer, additional_length)

			command_buffer.extend(device.generate_mac(bytes(command_buffer), True)[0:4])
		else:
			command_buffer.extend(self.data())

		command_buffer.append(0x00)
		if device.message_control.use_crc:
			command_buffer.append(0x00)

		self.add_packet_length(command_buffer)

		if device.message_control.use_crc:
			self.add_crc(command_buffer)
		else:
			self.add_checksum(command_buffer)

		custom_command_update(command_buffer)

		return bytes(command_buffer)

class PollCommand(Command):

	def __init__(self, address: int):
		self.address = address

	def command_code(self) -> int:
		return 0x60

	def security_control_block(self) -> bytes:
		return bytes([ 0x02, 0x15 ])

	def data() -> bytes:
		return bytes([])

	def custom_command_update(self, command_buffer: bytearray):
		pass

class IdReportCommand(Command):

	def __init__(self, address: int):
		self.address = address

	def command_code(self) -> int:
		return 0x61

	def security_control_block(self) -> bytes:
		return bytes([ 0x02, 0x17 ])

	def data() -> bytes:
		return bytes([ 0x00 ])

	def custom_command_update(self, command_buffer: bytearray):
		pass

class DeviceCapabilitiesCommand(Command):

	def __init__(self, address: int):
		self.address = address

	def command_code(self) -> int:
		return 0x62

	def security_control_block(self) -> bytes:
		return bytes([ 0x02, 0x17 ])

	def data() -> bytes:
		return bytes([ 0x00 ])

	def custom_command_update(self, command_buffer: bytearray):
		pass

class LocalStatusReportCommand(Command):

	def __init__(self, address: int):
		self.address = address

	def command_code(self) -> int:
		return 0x64

	def security_control_block(self) -> bytes:
		return bytes([ 0x02, 0x15 ])

	def data() -> bytes:
		return bytes([])

	def custom_command_update(self, command_buffer: bytearray):
		pass

class InputStatusReportCommand(Command):

	def __init__(self, address: int):
		self.address = address

	def command_code(self) -> int:
		return 0x65

	def security_control_block(self) -> bytes:
		return bytes([ 0x02, 0x15 ])

	def data() -> bytes:
		return bytes([ ])

	def custom_command_update(self, command_buffer: bytearray):
		pass


class OutputStatusReportCommand(Command):

	def __init__(self, address: int):
		self.address = address

	def command_code(self) -> int:
		return 0x66

	def security_control_block(self) -> bytes:
		return bytes([ 0x02, 0x15 ])

	def data() -> bytes:
		return bytes([])

	def custom_command_update(self, command_buffer: bytearray):
		pass

class ReaderStatusReportCommand(Command):

	def __init__(self, address: int):
		self.address = address

	def command_code(self) -> int:
		return 0x67

	def security_control_block(self) -> bytes:
		return bytes([ 0x02, 0x15 ])

	def data() -> bytes:
		return bytes([])

	def custom_command_update(self, command_buffer: bytearray):
		pass


class OutputControlCommand(Command):

	def __init__(self, address: int, output_controls: OutputControls):
		self.address = address
		self.output_controls = output_controls

	def command_code(self) -> int:
		return 0x68

	def security_control_block(self) -> bytes:
		return bytes([ 0x02, 0x17 ])

	def data() -> bytes:
		return self.output_controls.build_data()

	def custom_command_update(self, command_buffer: bytearray):
		pass


class ReaderLedControlCommand(Command):

	def __init__(self, address: int, reader_led_controls: ReaderLedControls):
		self.address = address
		self.reader_led_controls = reader_led_controls

	def command_code(self) -> int:
		return 0x69

	def security_control_block(self) -> bytes:
		return bytes([ 0x02, 0x17 ])

	def data() -> bytes:
		return self.reader_led_controls.build_data()

	def custom_command_update(self, command_buffer: bytearray):
		pass

class SecurityInitializationRequestCommand(Command):

	def __init__(self, address: int, server_random_number: bytes):
		self.address = address
		self.server_random_number = server_random_number

	def command_code(self) -> int:
		return 0x76

	def security_control_block(self) -> bytes:
		return bytes([ 0x03, 0x11, 0x00 ])

	def data() -> bytes:
		return self.server_random_number

	def custom_command_update(self, command_buffer: bytearray):
		pass


class ServerCryptogramCommand(Command):

	def __init__(self, address: int, server_cryptogram: bytes):
		self.address = address
		self.server_cryptogram = server_cryptogram

	def command_code(self) -> int:
		return 0x77

	def security_control_block(self) -> bytes:
		return bytes([ 0x03, 0x13, 0x00 ])

	def data() -> bytes:
		return self.server_cryptogram

	def custom_command_update(self, command_buffer: bytearray):
		pass
