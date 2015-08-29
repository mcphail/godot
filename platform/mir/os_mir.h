#ifndef OS_MIR_H
#define OS_MIR_H

#include "drivers/unix/os_unix.h"

class OS_Mir : public OS_Unix
{
public:
	virtual String get_data_dir() const;
};

#endif
