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

