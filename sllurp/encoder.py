import struct

class EncodingError (Exception):
    pass

class ReaderCommand (object):
    msg_type = None
    message_id = 0

    fields = (
        # (name, struct fmt, (start bit index, len))
        ('MessageType', '!H', (6, 10)),
        ('MessageLength', '!I', (0, 32)),
        ('MessageID', '!I', (0, 32)),
    )

    def __init__ (self, msg_dict):
        """
        Arguments:
            msg_dict: A dictionary of field values.  Must contain values for all
                fields except for MessageLength, MessageType, and MessageID, all
                of which self.encode() will fill in automatically.

        For fields that have their own encoding schemes defined, e.g., command
        parameters, pass an instance of a class that subclasses ReaderCommand.

        Example for an ADD_ACCESSSPEC command:

            # ACCESS_SPEC is a subclass of ReaderCommand
            access_spec = ACCESS_SPEC(...)

            # ADD_ACCESSSPEC is also a subclass of ReaderCommand
            add_accessspec = ADD_ACCESSSPEC({'AccessSpec': access_spec})
            as_bytes = add_accessspec.encode()
        """

    def encode (self, as_dict):
        # TODO: add docstring about auto-filling some fields
        # TODO: auto-fill fields
        data = ''
        for field_name, struct_fmt, (bit_index, len_bits) in self.fields:
            value = as_dict[field_name]
            data += struct.pack(struct_fmt, value)
        return data

    def decode (self, as_bytes):
        # TODO: write me
        return {}
