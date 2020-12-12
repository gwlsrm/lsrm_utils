import matplotlib.pyplot as plt
import speparser
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit()
    spectr = speparser.SpectrumReader.parse_spe(sys.argv[1])
    fig = plt.figure()
    plt.plot(list(range(len(spectr.spectr))), spectr.spectr)
    plt.show()

