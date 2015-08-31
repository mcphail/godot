#include "os_mir.h"
#include "main/main.h"
#include "servers/visual/visual_server_raster.h"
#include "servers/visual/visual_server_wrap_mt.h"
#include "drivers/gles2/rasterizer_gles2.h"

// Herein lies the skeleton of a class, to be embodied at a later date
void OS_Mir::initialize(const VideoMode &p_desired, int p_video_driver,
                        int p_audio_driver)
{
	rasterizer = memnew(RasterizerGLES2);
	visual_server = memnew(VisualServerRaster(rasterizer));
	if (get_render_thread_mode() != RENDER_THREAD_UNSAFE) {
		visual_server = memnew(VisualServerWrapMT(visual_server,
		           get_render_thread_mode() == RENDER_SEPARATE_THREAD));
	}
	visual_server->init();
}

void OS_Mir::set_main_loop(MainLoop *p_main_loop)
{
}

void OS_Mir::delete_main_loop()
{
}

void OS_Mir::finalize()
{
}

Point2 OS_Mir::get_mouse_pos() const
{
	Point2 sham;
	return sham;
}

int OS_Mir::get_mouse_button_state() const
{
	return 0;
}

void OS_Mir::set_window_title(const String &p_title)
{
}

void OS_Mir::set_video_mode(const VideoMode &p_video_mode, int p_screen)
{
}

OS_Mir::VideoMode OS_Mir::get_video_mode(int p_screen) const
{
	OS_Mir::VideoMode sham;
	return sham;
}

void OS_Mir::get_fullscreen_mode_list(List<VideoMode> *p_list,
                                      int p_screen) const
{
}

Size2 OS_Mir::get_window_size() const
{
	Size2 sham;
	return sham;
}

MainLoop *OS_Mir::get_main_loop() const
{
	MainLoop sham, *shamptr;
	shamptr = &sham;
	return shamptr;
}

bool OS_Mir::can_draw() const
{
	return false;
}

void OS_Mir::set_cursor_shape(CursorShape p_shape)
{
}
// Everything below this line should be flesh, rather than bone
int OS_Mir::get_video_driver_count() const
{
	return 1;
}

const char *OS_Mir::get_video_driver_name(int index) const
{
	return "GLES2";
}

OS_Mir::VideoMode OS_Mir::get_default_video_mode() const
{
	return OS::VideoMode(800, 600, false);
}

String OS_Mir::get_data_dir() const
{
	// Ubuntu phone apps are confined by apparmor to certain directories
	String app_id = get_environment("APP_ID");
	String app_pkgname = app_id.get_slice(String("_"), 0);
	return (get_environment(String("XDG_DATA_DIR"))
	        + String("/") + app_pkgname);
}

void OS_Mir::run()
{
	// main_loop is set if Main::start() has succeded
	if (! main_loop) {
		return;
	}
	main_loop->init();

	while (! Main::iteration()) {
	}

	main_loop->finish();
}
