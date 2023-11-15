from anta.models import AntaTest, AntaCommand


class VerifyLACP(AntaTest):
    """
    Verify LACP status
    """

    name = "VerifyLACP"
    description = "Verifies LACP status."
    categories = ["interfaces"]
    commands = [AntaCommand(command="show lacp interface all-ports brief", ofmt="json")]

    @AntaTest.anta_test
    def test(self) -> None:
        command_output = self.instance_commands[0].json_output
        
        failed_ports = list()
        for port_channel_name, port_channel_interfaces in command_output["portChannels"].items():
            for interface_name, interface_lacp_status in port_channel_interfaces["interfaces"].items():
                if interface_lacp_status["actorPortStatus"] != "bundled":
                    failed_ports.append(interface_name)

        if len(failed_ports):
            self.result.is_failure(f"List of not bundled interfaces : '{failed_ports}'")
        else:
            self.result.is_success()

class VerifyRouteCount(AntaTest):
    """
    Verify number of routes in the VRF
    """

    name = "VerifyRouteCount"
    description = "Verifies route count in a VRF"
    categories = ["routing", "generic"]
    commands = [AntaCommand(command="show ip route vrf all summary", revision=3)]

    class Input(AntaTest.Input):  # pylint: disable=missing-class-docstring
        vrf: str = "default"
        minimum: int
        """Expected minimum routing table (default VRF) size"""
        maximum: int
        """Expected maximum routing table (default VRF) size"""

    @AntaTest.anta_test
    def test(self) -> None:
        command_output = self.instance_commands[0].json_output
        total_routes = int(command_output["vrfs"][self.inputs.vrf]["connected"])
        if self.inputs.minimum <= total_routes <= self.inputs.maximum:
            self.result.is_success()
        else:
            self.result.is_failure(f"routing-table has {total_routes} routes and not between min ({self.inputs.minimum}) and maximum ({self.inputs.maximum})")

