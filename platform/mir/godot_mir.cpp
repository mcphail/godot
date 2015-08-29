#include "main/main.h"
#include "os_mir.h"

int main(int argc, char **argv)
{
	OS_Mir os;

	Error err = Main::setup(argv[0], argc-1, &argv[1]);
	if (err != OK) {
		return 255;
	}

	if (Main::start()) {
		os.run();
	}

	Main::cleanup();
	return 0;
}
