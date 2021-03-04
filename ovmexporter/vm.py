from cliff.lister import Lister
from cliff.show import ShowOne


class VirtualMachines(Lister):

    def get_parser(self, prog_name):
        parser = super(VirtualMachines, self).get_parser(prog_name)
        return parser

    def take_action(self, args):
        vms = self._ovm_client.get_vms()
        ret = [
            ["ID", "Friendly Name", "Snapshots"]
        ]
        items = []
        for vm in vms:
            item = [
                vm["name"],
                vm["friendly_name"],
                "\n".join(vm["snapshots"])
            ]
            items.append(item)

        ret.append(items)
        return ret


class ShowVirtualMachine(ShowOne):

    def get_parser(self, prog_name):
        parser = super(ShowVirtualMachine, self).get_parser(prog_name)
        parser.add_argument("id", help="The ID of the VM")
        return parser
    
    def take_action(self, args):
        vm = self._ovm_client.get_vm(args.id)
        columns = ('ID',
                   'Friendly name',
                   'UUID',
                   'Disks',
                   'Snapshots')
        data = (vm["name"],
                vm["friendly_name"],
                vm["uuid"],
                "\n".join([d["name"] for d in vm["disks"]]),
                "\n".join(vm["snapshots"]))
        return (columns, data)
