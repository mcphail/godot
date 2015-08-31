
import os
import sys	


def is_active():
	return True
        
def get_name():
        return "Mir"


def can_build():

	if (os.name!="posix"):
		return False

	if sys.platform == "darwin":
		return False # no Mir on mac for now

	errorval=os.system("pkg-config --version > /dev/null")
	
	if (errorval):
		print("pkg-config not found.. Mir disabled.")
		return False
	
	mir_error=os.system("pkg-config mirclient --modversion > /dev/null ")
	if (mir_error):
		print("Mirclient not found.. Mir disabled.")
		return False

        ssl_error=os.system("pkg-config openssl --modversion > /dev/null ")
        if (ssl_error):
                print("OpenSSL not found.. Mir disabled.")
                return False

	mir_error=os.system("pkg-config xcursor --modversion > /dev/null ")
	if (mir_error):
		print("xcursor not found.. Mir disabled.")
		return False
	
	#x11_error=os.system("pkg-config xinerama --modversion > /dev/null ")
	#if (x11_error):
	#	print("xinerama not found.. x11 disabled.")
	#	return False

	
	return True # Mir enabled
  
def get_opts():

	return [
	('use_llvm','Use llvm compiler','no'),
	('use_sanitizer','Use llvm compiler sanitize address','no'),
	('use_leak_sanitizer','Use llvm compiler sanitize memory leaks','no'),
	('pulseaudio','Detect & Use pulseaudio','yes'),
	('new_wm_api', 'Use experimental window management API','no'),
	('debug_release', 'Add debug symbols to release version','no'),
	]
  
def get_flags():

	return [
	('builtin_zlib', 'no'),
	("openssl", "yes"),
	("theora","no"),
        ]
			


def configure(env):

	is64=sys.maxsize > 2**32

	if (env["bits"]=="default"):
		if (is64):
			env["bits"]="64"
		else:
			env["bits"]="32"

	env.Append(CPPPATH=['#platform/mir'])
	if (env["use_llvm"]=="yes"):
		if 'clang++' not in env['CXX']:
			env["CC"]="clang"
			env["CXX"]="clang++"
			env["LD"]="clang++"
		env.Append(CPPFLAGS=['-DTYPED_METHOD_BIND'])
		env.extra_suffix=".llvm"

		if (env["colored"]=="yes"):
			if sys.stdout.isatty():
				env.Append(CXXFLAGS=["-fcolor-diagnostics"])

	if (env["use_sanitizer"]=="yes"):
		env.Append(CXXFLAGS=['-fsanitize=address','-fno-omit-frame-pointer'])
		env.Append(LINKFLAGS=['-fsanitize=address'])
		env.extra_suffix+="s"

	if (env["use_leak_sanitizer"]=="yes"):
		env.Append(CXXFLAGS=['-fsanitize=address','-fno-omit-frame-pointer'])
		env.Append(LINKFLAGS=['-fsanitize=address'])
		env.extra_suffix+="s"


	#if (env["tools"]=="no"):
	#	#no tools suffix
	#	env['OBJSUFFIX'] = ".nt"+env['OBJSUFFIX']
	#	env['LIBSUFFIX'] = ".nt"+env['LIBSUFFIX']


	if (env["target"]=="release"):

		if (env["debug_release"]=="yes"):
			env.Append(CCFLAGS=['-g2'])
		else:
			env.Append(CCFLAGS=['-O3','-ffast-math'])

	elif (env["target"]=="release_debug"):

		env.Append(CCFLAGS=['-O2','-ffast-math','-DDEBUG_ENABLED'])

	elif (env["target"]=="debug"):

		env.Append(CCFLAGS=['-g2', '-Wall','-DDEBUG_ENABLED','-DDEBUG_MEMORY_ENABLED'])

	env.ParseConfig('pkg-config mirclient --cflags --libs')
	#env.ParseConfig('pkg-config xinerama --cflags --libs')
	env.ParseConfig('pkg-config xcursor --cflags --libs')

	if (env["openssl"]=="yes"):
		env.ParseConfig('pkg-config openssl --cflags --libs')


	env.ParseConfig('pkg-config freetype2 --cflags --libs')
	env.Append(CCFLAGS=['-DFREETYPE_ENABLED'])

	
	#env.Append(CPPFLAGS=['-DOPENGL_ENABLED','-DGLEW_ENABLED'])
	env.Append(CPPFLAGS=["-DALSA_ENABLED"])

	if (env["pulseaudio"]=="yes"):
		if not os.system("pkg-config --exists libpulse-simple"):
			print("Enabling PulseAudio")
			env.Append(CPPFLAGS=["-DPULSEAUDIO_ENABLED"])
			env.ParseConfig('pkg-config --cflags --libs libpulse-simple')
		else:
			print("PulseAudio development libraries not found, disabling driver")

	env.Append(CPPFLAGS=['-DUNIX_ENABLED','-DGLES2_ENABLED'])
	env.Append(LIBS=['GLESv2','pthread','asound','z']) #TODO detect linux/BSD!
	#env.Append(CPPFLAGS=['-DMPC_FIXED_POINT'])

#host compiler is default..

	if (is64 and env["bits"]=="32"):
		env.Append(CPPFLAGS=['-m32'])
		env.Append(LINKFLAGS=['-m32','-L/usr/lib/i386-linux-gnu'])
	elif (not is64 and env["bits"]=="64"):
		env.Append(CPPFLAGS=['-m64'])
		env.Append(LINKFLAGS=['-m64','-L/usr/lib/i686-linux-gnu'])


	import methods

	env.Append( BUILDERS = { 'GLSL120' : env.Builder(action = methods.build_legacygl_headers, suffix = 'glsl.h',src_suffix = '.glsl') } )
	env.Append( BUILDERS = { 'GLSL' : env.Builder(action = methods.build_glsl_headers, suffix = 'glsl.h',src_suffix = '.glsl') } )
	env.Append( BUILDERS = { 'GLSL120GLES' : env.Builder(action = methods.build_gles2_headers, suffix = 'glsl.h',src_suffix = '.glsl') } )
	#env.Append( BUILDERS = { 'HLSL9' : env.Builder(action = methods.build_hlsl_dx9_headers, suffix = 'hlsl.h',src_suffix = '.hlsl') } )

	#if(env["new_wm_api"]=="yes"):
	#	env.Append(CPPFLAGS=['-DNEW_WM_API'])
	#	env.ParseConfig('pkg-config xinerama --cflags --libs')
