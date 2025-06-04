# Ringtail

This is a pure Golang implementation of Ringtail [eprint.iacr.org/2024/1113](https://eprint.iacr.org/2024/1113), a practical two-round threshold signature scheme from LWE.

**WARNING:** This implementation is an academic proof-of-concept prototype, has not received careful code review, and is not ready for production use.

## Getting Started

The project requires **Go 1.19** or later. The commands below show how to set up
and run the code on a typical Ubuntu system.

### Installation

1. Install Go using the package manager (or download it from the [official Go
   website](https://go.dev/dl/)):

   ```bash
   sudo apt update
   sudo apt install -y golang-go
   ```

2. Clone the repository and download the Go module dependencies:

   ```bash
   git clone https://github.com/daryakaviani/ringtail.git
   cd ringtail
   go mod download
   ```

### Running

You can run the scheme locally (all parties on a single machine) or as separate
processes communicating over the network.

#### Local Mode

Run all parties on your machine using the special party id `l`. The second
argument is the number of iterations to average over. The third argument is the
number of parties:

```bash
go run main.go l 1 3
```

#### Networked Mode

To run parties on separate terminals or machines, give each process a unique
party id between `0` and `parties-1` and specify the total number of parties. For
example, with three parties run the following in three different terminals or
hosts:

```bash
go run main.go 0 1 3
go run main.go 1 1 3
go run main.go 2 1 3
```

You can also build a binary instead of using `go run`:

```bash
go build -o ringtail
./ringtail <partyID> <iters> <parties>
```

### Automated Setup and Testing

Run the Python helper script to install Go (if needed), download the Go modules, build the project, and run a local signing round to verify everything works:

```bash
python3 scripts/setup_and_test.py
```

### Codebase Overview
- `networking/`
    - `networking.go`: Includes the networking stack which allows signers to form peer-to-peer network connections with other parties. Each party concurrently communicates with every other party by serializing and sending its messages through outgoing TCP sockets, while simultaneously receiving and processing incoming messages.
- `primitives/`
    - `hash.go`: Hashes, MACs, PRFs involved in the scheme.
    - `shamir.go`: Shamir secret-sharing for secret key vector.
- `sign/`
    - `config.go`: Parameters for concrete instantiation.
    - `local.go`: Locally runs the scheme on a single machine for a given number of parties.
    - `sign.go`: Core functionality of the scheme.
- `utils/`
    - `utils.go`: Helpers related to NTT and Montgomery conversions, multiplying, and initializing matrices and vectors of ring elements.
    - `utils-naive.go`: This is not used in the current version, but can be used for testing. It implements convolution-based naive ring-element multiplication.
- `main.go`: Run the code with `go run main.go id iters parties` where `id` is the party ID of the signer running the code (use `l` if you want to run the scheme locally), `iters` is the number of iterations to average the latencies over if you are benchmarking (if not, just use 1), and `parties` is the total number of parties. This is currently a full-threshold implementation. For testing a smaller threshold, set the `Threshold` config parameter with a different value, and use `ShamirSecretSharingGeneral`.

### License

Ringtail is licensed under the Apache 2.0 License. See [LICENSE](https://github.com/daryakaviani/ringtail/blob/main/LICENSE).
