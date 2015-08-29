#ifndef OS_MIR_H
#define OS_MIR_H

#include "drivers/unix/os_unix.h"

class OS_Mir : public OS_Unix
{
	MainLoop *main_loop;

protected:
	int get_video_driver_count() const;
	const char *get_video_driver_name(int p_driver) const;
	VideoMode get_default_video_mode() const;
	void initialize(const VideoMode &p_desired, int p_video_driver,
	                int p_audio_driver);
	void set_main_loop(MainLoop *p_main_loop);
	void delete_main_loop();
	void finalize();
public:
	Point2 get_mouse_pos() const;
	int get_mouse_button_state() const;
	void set_window_title(const String &p_title);
	void set_video_mode(const VideoMode &p_video_mode, int p_screen=0);
	VideoMode get_video_mode(int p_screen=0) const;
	void get_fullscreen_mode_list(List<VideoMode> *p_list,
	                              int p_screen=0) const;
	Size2 get_window_size() const;
	MainLoop *get_main_loop() const;
	bool can_draw() const;
	void set_cursor_shape(CursorShape p_shape);

	String get_data_dir() const;
	// Called by godot_mir.cpp in the main function
	void run();
};

#endif
