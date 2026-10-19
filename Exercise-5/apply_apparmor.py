import docker

client = docker.from_env()

print("Building flask-apparmor image...")
client.images.build(path=".", tag="flask-apparmor")

try:
    old = client.containers.get("flask-apparmor-demo")
    old.remove(force=True)
except docker.errors.NotFound:
    pass

container = client.containers.run(
    "flask-apparmor",
    name="flask-apparmor-demo",
    ports={"5000/tcp": 5000},
    security_opt=["apparmor=my-apparmor-profile"],
    detach=True
)

try:
    info = client.api.inspect_container(container.id)
    print("Container started:", container.short_id)
    print("Security options:", info["HostConfig"].get("SecurityOpt"))
    print("Reported AppArmor profile:", info.get("AppArmorProfile"))
finally:
    container.stop()
    container.remove()
    print("Container stopped and removed.")
