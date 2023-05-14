import typer
import uuid
from nostr import Client, Event


app = typer.Typer()


@app.command()
def publish_event(
    content: str = "hello",
    event_type: int = 1,
    url: str = "ws://0.0.0.0:8001",
    public_key: str = "d0b69840e1a7f1f19a4227c0311ffd42e28ddd277b2e259fb64e6a2e559bb408",
    private_key: str = "ca52acacfbfbf9f040de69361a2c1ea78b705399ce909d4a5a87e7bc029cead7",
):
    client = Client(url=url, private_key=private_key)
    client.open_connection()

    event = Event(
        content=content,
        kind=event_type,
        public_key=public_key,
    )
    client.publish_event(event)
    client.add_subscription()


if __name__ == "__main__":
    app()
