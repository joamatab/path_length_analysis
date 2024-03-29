from path_analysis import path_length
import gdsfactory as gf


def routes():
    ys_right = [0, 10, 20, 40, 50, 80]
    pitch = 127.0
    N = len(ys_right)
    ys_left = [(i - N / 2) * pitch for i in range(N)]
    layer = (1, 0)

    right_ports = [
        gf.Port(
            f"R_{i}", center=(0, ys_right[i]), width=0.5, orientation=180, layer=layer
        )
        for i in range(N)
    ]
    left_ports = [
        gf.Port(
            f"L_{i}", center=(-200, ys_left[i]), width=0.5, orientation=0, layer=layer
        )
        for i in range(N)
    ]

    # you can also mess up the port order and it will sort them by default
    left_ports.reverse()

    c = gf.Component(name="connect_bundle_v2")
    routes = gf.routing.get_bundle(
        left_ports,
        right_ports,
        sort_ports=True,
        start_straight_length=100,
        enforce_port_ordering=False,
    )
    for i, route in enumerate(routes):
        c.add(route.references)
        gf.add_pins.add_pin_rectangle(c, port=route.ports[0], layer=(2,0))
        gf.add_pins.add_pin_rectangle(c, port=route.ports[1], layer=(2,0))
        c.add_label(f"i{i}", position=route.ports[0].center, layer=(2,0))
        c.add_label(f"o{i}", position=route.ports[1].center, layer=(2,0))
    return c


if __name__ == "__main__":
    c = routes()
    # c = c.flatten()
    # c.name= 'connect_bundle'
    c.show()
    gdspath = c.write_gds("demo.gds")
    # nodes = []
    # nodes += [f"i{i}" for i in range(4)]
    # nodes += [f"o{i}" for i in range(4)]
    labels = [('i0', 'o0')]

    df = path_length(
        gdspath,
        path_layer=(1, 0),
        label_layer=(2, 0),
        labels=labels
    )
    c.show()
