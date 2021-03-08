from cliff.lister import Lister
from cliff.show import ShowOne

from ovmexporter import client


class VirtualMachines(Lister):

    def get_parser(self, prog_name):
        parser = super(VirtualMachines, self).get_parser(prog_name)
        return parser

    def take_action(self, args):
        cli = client.get_client_from_options(
            self._cmd_options)
        vms = cli.get_vms()
        ret = [
            ["ID", "Friendly Name", "Snapshot compatible", "Snapshots"]
        ]
        items = []
        for vm in vms:
            item = [
                vm["name"],
                vm["friendly_name"],
                vm["snapshot_compatible"],
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
        cli = client.get_client_from_options(
            self._cmd_options)
        vm = cli.get_vm(args.id)
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
