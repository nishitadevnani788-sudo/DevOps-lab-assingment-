import docker

client = docker.from_env()
container = client.containers.run(
    "flask-apparmor",
    security_opt=["apparmor=my-apparmor-profile"],
    detach=True
)

try:
    info = client.api.inspect_container(container.id)
    print("Container started:", container.short_id)
    print("Security options:", info["HostConfig"].get("SecurityOpt"))
    print("Reported AppArmor profile:", info.get("AppArmorProfile"))

    for command in [
        ["cat", "/etc/passwd"],
        ["/bin/bash"]
    ]:
        result = container.exec_run(command)
        print("\nCommand:", command)
        print("Exit code:", result.exit_code)
        print("Output:", result.output.decode(errors="replace") or "(no output)")
finally:
    container.stop()
    container.remove()
    print("Container stopped and removed.")
