#include "os_mir.h"

String OS_Mir::get_data_dir() const
{
	String app_id = get_environment("APP_ID");
	String app_pkgname = app_id.get_slice(String("_"), 0);
	return (get_environment(String("XDG_DATA_DIR"))
	        + String("/") + app_pkgname);
}
