import struct

class EncodingError (Exception):
    pass

class SllurpMessage (object):
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
        parameters, pass an instance of a class that subclasses SllurpMessage.

        Example for an ADD_ACCESSSPEC command:

            # ACCESS_SPEC is a subclass of SllurpMessage
            access_spec = ACCESS_SPEC(...)

            # ADD_ACCESSSPEC is also a subclass of SllurpMessage
            add_accessspec = ADD_ACCESSSPEC({'AccessSpec': access_spec})
            as_bytes = add_accessspec.encode()
        """
        self.msg_dict = msg_dict

    def encode (self):
        """Returns the binary LLRP representation of this SllurpMessage.
        Automatically fills the MessageLength, MessageType, and MessageID
        fields."""

        data = ''

        # fill MessageID field
        self.msg_dict['MessageID'] = SllurpMessage.next_message_id()
        self.msg_dict['MessageType'] = self.msg_type
        self.msg_dict['MessageLength'] = 0 # will be computed last

        len_field_pos = None

        # iterate through all fields in the message type, building up the data
        # string one field at a time
        for field_name, struct_fmt, (bit_index, len_bits) in self.fields:
            if field_name == 'MessageLength':
                len_field_pos = len(data)
            value = self.msg_dict[field_name]
            fieldwidth_bits = 8 * struct.calcsize(struct_fmt)
            assert(len_bits <= fieldwidth_bits)
            shiftwidth = fieldwidth_bits - bit_index - len_bits
            if isinstance(value, int) and shiftwidth:
                value <<= shiftwidth
            data += struct.pack(struct_fmt, value)

        # patch up MessageLength field with the final length
        data = data[ : len_field_pos] + struct.pack('!I', len(data)) + \
            data[len_field_pos + struct.calcsize('!I') : ]

        return data

    def decode (self, as_bytes):
        # TODO: write me
        return {}

    @classmethod
    def next_message_id (_):
        SllurpMessage.message_id += 1
        return SllurpMessage.message_id
