def _CFRunLoopServiceMachPort_hook(hilda, *args):
    """
    :param hilda.hilda_client.HildaClient hilda:
    """
    hilda.registers.pc = hilda.CFRunLoopServiceMachPort_while_ea
    hilda.cont()


def disable_mach_msg_errors(self):
    """
    Disable the error check inside the CFRunLoopServiceMachPort from the mach_msg syscall.
    This is used to debug slow handling of mach messages.
    :param hilda.hilda_client.HildaClient self: Hilda client.
    """
    with self.stopped():
        instructions = self.symbols.__CFRunLoopServiceMachPort.disass(2000, should_print=False)
        while_ea = None
        for instruction in instructions:
            if (while_ea is None) and instruction.DoesBranch():
                # Beginning of the `while(true) { ... }`
                while_ea = instruction.GetOperands(self.target)
                self.CFRunLoopServiceMachPort_while_ea = int(self.file_symbol(eval(while_ea)))
            elif instruction.GetMnemonic(self.target) == 'brk':
                symbol = self.symbol(instruction.addr.GetLoadAddress(self.target))
                symbol.bp(
                    _CFRunLoopServiceMachPort_hook,
                    forced=True,
                    name=f'__CFRunLoopServiceMachPort-brk-{int(symbol - self.symbols.__CFRunLoopServiceMachPort)}'
                )
