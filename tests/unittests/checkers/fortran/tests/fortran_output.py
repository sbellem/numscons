g77_link_output = """
Driving: g77 -v empty.o -o empty -lfrtbegin -lg2c -lm -shared-libgcc
Reading specs from /usr/lib/gcc/i486-linux-gnu/3.4.6/specs
Configured with: ../src/configure -v --enable-languages=c,c++,f77,pascal --prefix=/usr --libexecdir=/usr/lib --with-gxx-include-dir=/usr/include/c++/3.4 --enable-shared --with-system-zlib --enable-nls --without-included-gettext --program-suffix=-3.4 --enable-__cxa_atexit --enable-clocale=gnu --enable-libstdcxx-debug --with-tune=pentium4 i486-linux-gnu
Thread model: posix
gcc version 3.4.6 (Ubuntu 3.4.6-6ubuntu1)
 /usr/lib/gcc/i486-linux-gnu/3.4.6/collect2 --eh-frame-hdr -m elf_i386 -dynamic-linker /lib/ld-linux.so.2 -o empty /usr/lib/gcc/i486-linux-gnu/3.4.6/../../../../lib/crt1.o /usr/lib/gcc/i486-linux-gnu/3.4.6/../../../../lib/crti.o /usr/lib/gcc/i486-linux-gnu/3.4.6/crtbegin.o -L/usr/lib/gcc/i486-linux-gnu/3.4.6 -L/usr/lib/gcc/i486-linux-gnu/3.4.6 -L/usr/lib/gcc/i486-linux-gnu/3.4.6/../../../../lib -L/usr/lib/gcc/i486-linux-gnu/3.4.6/../../.. -L/lib/../lib -L/usr/lib/../lib empty.o -lfrtbegin -lg2c -lm -lgcc_s -lgcc -lc -lgcc_s -lgcc /usr/lib/gcc/i486-linux-gnu/3.4.6/crtend.o /usr/lib/gcc/i486-linux-gnu/3.4.6/../../../../lib/crtn.o"""

g77_link_expected = ['-L/usr/lib/gcc/i486-linux-gnu/3.4.6',
        '-L/usr/lib/gcc/i486-linux-gnu/3.4.6',
        '-L/usr/lib/gcc/i486-linux-gnu/3.4.6/../../../../lib',
        '-L/usr/lib/gcc/i486-linux-gnu/3.4.6/../../..', '-L/lib/../lib',
        '-L/usr/lib/../lib', '-lfrtbegin', '-lg2c', '-lm']

g77_link_parsed = {'LIBPATH' :['/usr/lib/gcc/i486-linux-gnu/3.4.6',
        '/usr/lib/gcc/i486-linux-gnu/3.4.6',
        '/usr/lib/gcc/i486-linux-gnu/3.4.6/../../../../lib',
        '/usr/lib/gcc/i486-linux-gnu/3.4.6/../../..', '/lib/../lib',
        '/usr/lib/../lib'], 
	'LIBS': ['frtbegin', 'g2c', 'm']}

gfortran_link_output = """
Driving: gfortran -v -o hello hello.o -lgfortranbegin -lgfortran -lm -shared-libgcc
Using built-in specs.
Target: i486-linux-gnu
Configured with: ../src/configure -v --enable-languages=c,c++,fortran,objc,obj-c++,treelang --prefix=/usr --enable-shared --with-system-zlib --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --enable-nls --with-gxx-include-dir=/usr/include/c++/4.2 --program-suffix=-4.2 --enable-clocale=gnu --enable-libstdcxx-debug --enable-mpfr --enable-targets=all --enable-checking=release --build=i486-linux-gnu --host=i486-linux-gnu --target=i486-linux-gnu
Thread model: posix
gcc version 4.2.1 (Ubuntu 4.2.1-5ubuntu4)
 /usr/lib/gcc/i486-linux-gnu/4.2.1/collect2 --eh-frame-hdr -m elf_i386 --hash-style=both -dynamic-linker /lib/ld-linux.so.2 -o hello /usr/lib/gcc/i486-linux-gnu/4.2.1/../../../../lib/crt1.o /usr/lib/gcc/i486-linux-gnu/4.2.1/../../../../lib/crti.o /usr/lib/gcc/i486-linux-gnu/4.2.1/crtbegin.o -L/usr/lib/gcc/i486-linux-gnu/4.2.1 -L/usr/lib/gcc/i486-linux-gnu/4.2.1 -L/usr/lib/gcc/i486-linux-gnu/4.2.1/../../../../lib -L/lib/../lib -L/usr/lib/../lib -L/usr/lib/gcc/i486-linux-gnu/4.2.1/../../.. hello.o -lgfortranbegin -lgfortran -lm -lgcc_s -lgcc -lc -lgcc_s -lgcc /usr/lib/gcc/i486-linux-gnu/4.2.1/crtend.o /usr/lib/gcc/i486-linux-gnu/4.2.1/../../../../lib/crtn.o"""

gfortran_link_expected = ['-L/usr/lib/gcc/i486-linux-gnu/4.2.1',
        '-L/usr/lib/gcc/i486-linux-gnu/4.2.1',
        '-L/usr/lib/gcc/i486-linux-gnu/4.2.1/../../../../lib', '-L/lib/../lib',
        '-L/usr/lib/../lib', '-L/usr/lib/gcc/i486-linux-gnu/4.2.1/../../..',
        '-lgfortranbegin', '-lgfortran', '-lm']

sunfort_v12_link_output = """
NOTICE: Invoking /home/david/opt/sun/sunstudio12/bin/f90 -f77 -ftrap=%none -c empty.f
###     command line files and options (expanded):
    ### -f77=%all -ftrap=%none -v empty.o 
    ### f90: Note: NLSPATH = /home/david/opt/sun/sunstudio12/prod/bin/../lib/locale/%L/LC_MESSAGES/%N.cat:/home/david/opt/sun/sunstudio12/prod/bin/../../lib/locale/%L/LC_MESSAGES/%N.cat
    ### f90: Note: LD_LIBRARY_PATH = /home/david/local/intel/cc/9.1.042/lib:/home/david/local/lib:
    ### f90: Note: LD_RUN_PATH     = (null)
    ### f90: Note: LD_OPTIONS = (null)
    /usr/bin/ld -m elf_i386 -dynamic-linker /lib/ld-linux.so.2 --enable-new-dtags -R/home/david/opt/sun/sunstudio12/lib:/opt/sun/sunstudio12/lib:/home/david/opt/sun/lib/rtlibs:/opt/sun/lib/rtlibs -o a.out /home/david/opt/sun/sunstudio12/prod/lib/crti.o /home/david/opt/sun/sunstudio12/prod/lib/crt1.o /home/david/opt/sun/sunstudio12/prod/lib/values-xi.o -Y P,/home/david/opt/sun/sunstudio12/lib:/home/david/opt/sun/sunstudio12/rtlibs:/home/david/opt/sun/sunstudio12/prod/lib:/lib:/usr/lib empty.o -lfui -lfai -lfsu -Bdynamic -lmtsk -lpthread -lm -lc /home/david/opt/sun/sunstudio12/prod/lib/libc_supp.a /home/david/opt/sun/sunstudio12/prod/lib/crtn.o
    empty.f:
     MAIN hello:
"""

sunfort_v12_link_expected = ['-R/home/david/opt/sun/sunstudio12/lib:'\
        '/opt/sun/sunstudio12/lib:/home/david/opt/sun/lib/rtlibs:'\
        '/opt/sun/lib/rtlibs', '-L/home/david/opt/sun/sunstudio12/lib',
        '-L/home/david/opt/sun/sunstudio12/rtlibs',
        '-L/home/david/opt/sun/sunstudio12/prod/lib', '-L/lib', '-L/usr/lib',
        '-lfui', '-lfai', '-lfsu', '-lmtsk', '-lpthread', '-lm']

ifort_v10_link_output = """
ld    /usr/lib/gcc/i486-linux-gnu/4.1.3/../../../crt1.o /usr/lib/gcc/i486-linux-gnu/4.1.3/../../../crti.o /usr/lib/gcc/i486-linux-gnu/4.1.3/crtbegin.o --eh-frame-hdr -dynamic-linker /lib/ld-linux.so.2 -m elf_i386 -o a.out /home/david/opt/intel/fc/10.0.023//lib/for_main.o empty.o -L/home/david/opt/intel/fc/10.0.023//lib -L/usr/lib/gcc/i486-linux-gnu/4.1.3/ -L/usr/lib/gcc/i486-linux-gnu/4.1.3/../../../ -Bstatic -lifport -lifcore -limf -Bdynamic -lm -Bstatic -lipgo -lirc -Bdynamic -lc -lgcc_s -lgcc -Bstatic -lirc_s -Bdynamic -ldl -lc /usr/lib/gcc/i486-linux-gnu/4.1.3/crtend.o /usr/lib/gcc/i486-linux-gnu/4.1.3/../../../crtn.o
"""

ifort_v10_link_expected = ['-L/home/david/opt/intel/fc/10.0.023//lib',
        '-L/usr/lib/gcc/i486-linux-gnu/4.1.3/',
        '-L/usr/lib/gcc/i486-linux-gnu/4.1.3/../../../', '-lifport',
        '-lifcore', '-limf', '-lm', '-lipgo', '-lirc', '-lirc_s', '-ldl']

mingw_g77_link_output = """"""

mingw_g77_link_expected = ['-Lc:/MinGW/bin/../lib/gcc/mingw32/3.4.5 -Lc:/MinGW/bin/../lib/gcc -Lc:/MinGW/bin/../lib/gcc/mingw32/3.4.5/../../../../mingw32/lib -Lc:/MinGW/bin/../lib/gcc/mingw32/3.4.5/../../.. -lfrtbegin -lg2c -lmingw32 -lmoldname -lmingwex -lmsvcrt -luser32 -lkernel32 -ladvapi32 -lshell32']

mingw_gfortran_link_output = """
Driving: gfortran -v empty.o -lgfortranbegin -lgfortran
Using built-in specs.
Target: i386-pc-mingw32
Configured with: ../trunk/configure --prefix=/mingw --enable-languages=c,fortran --with-gmp=/home/FX/local --with-ld=/mingw/bin/ld --with-as=/mingw/bin/as --disable-werror --enable-bootstrap --enable-threads --disable-nls --build=i386-pc-mingw32 --enable-libgomp --disable-shared
Thread model: win32
gcc version 4.3.0 20080109 (experimental) [trunk revision 131426] (GCC) 
COMPILER_PATH=c:/program files/gfortran/bin/../libexec/gcc/i386-pc-mingw32/4.3.0/;c:/program files/gfortran/bin/../libexec/gcc/
LIBRARY_PATH=c:/program files/gfortran/bin/../lib/gcc/i386-pc-mingw32/4.3.0/;c:/program files/gfortran/bin/../lib/gcc/;c:/program files/gfortran/bin/../lib/gcc/i386-pc-mingw32/4.3.0/../../../;/mingw/lib/
COLLECT_GCC_OPTIONS='-v' '-mtune=i386'
 c:/program files/gfortran/bin/../libexec/gcc/i386-pc-mingw32/4.3.0/collect2.exe -Bdynamic c:/program files/gfortran/bin/../lib/gcc/i386-pc-mingw32/4.3.0/../../../crt2.o c:/program files/gfortran/bin/../lib/gcc/i386-pc-mingw32/4.3.0/crtbegin.o -Lc:/program files/gfortran/bin/../lib/gcc/i386-pc-mingw32/4.3.0 -Lc:/program files/gfortran/bin/../lib/gcc -Lc:/program files/gfortran/bin/../lib/gcc/i386-pc-mingw32/4.3.0/../../.. -L/mingw/lib empty.o -lgfortranbegin -lgfortran -lmingw32 -lgcc -lmoldname -lmingwex -lmsvcrt -luser32 -lkernel32 -ladvapi32 -lshell32 -lmingw32 -lgcc -lmoldname -lmingwex -lmsvcrt c:/program files/gfortran/bin/../lib/gcc/i386-pc-mingw32/4.3.0/crtend.o"""

cygwin_g77_link_output = """
Driving: g77 -v empty.o -lfrtbegin -lg2c
Reading specs from /usr/lib/gcc/i686-pc-cygwin/3.4.4/specs
Configured with: /usr/build/package/orig/test.respin/gcc-3.4.4-3/configure --verbose --prefix=/usr --exec-prefix=/usr --sysconfdir=/etc --libdir=/usr/lib --libexecdir=/usr/lib --mandir=/usr/share/man --infodir=/usr/share/info --enable-languages=c,ada,c++,d,f77,pascal,java,objc --enable-nls --without-included-gettext --enable-version-specific-runtime-libs --without-x --enable-libgcj --disable-java-awt --with-system-zlib --enable-interpreter --disable-libgcj-debug --enable-threads=posix --enable-java-gc=boehm --disable-win32-registry --enable-sjlj-exceptions --enable-hash-synchronization --enable-libstdcxx-debug
Thread model: posix
gcc version 3.4.4 (cygming special, gdc 0.12, using dmd 0.125)
 /usr/lib/gcc/i686-pc-cygwin/3.4.4/collect2.exe -Bdynamic --dll-search-prefix=cyg /usr/lib/gcc/i686-pc-cygwin/3.4.4/../../../crt0.o -L/usr/lib/gcc/i686-pc-cygwin/3.4.4 -L/usr/lib/gcc/i686-pc-cygwin/3.4.4 -L/usr/lib/gcc/i686-pc-cygwin/3.4.4/../../.. empty.o -lfrtbegin -lg2c -lgcc -lcygwin -luser32 -lkernel32 -ladvapi32 -lshell32 -lgcc"""

cygwin_g77_link_expected = ['-L/usr/lib/gcc/i686-pc-cygwin/3.4.4',
        '-L/usr/lib/gcc/i686-pc-cygwin/3.4.4',
        '-L/usr/lib/gcc/i686-pc-cygwin/3.4.4/../../..', '-lfrtbegin', '-lg2c',
        '-lcygwin',  '-luser32', '-lkernel32', '-ladvapi32', '-lshell32']

cygwin_g77_link_parsed = {'LIBPATH': ['/usr/lib/gcc/i686-pc-cygwin/3.4.4',
	'/usr/lib/gcc/i686-pc-cygwin/3.4.4',
	'/usr/lib/gcc/i686-pc-cygwin/3.4.4/../../..'],
	'LIBS': ['frtbegin', 'g2c', 'cygwin',  'user32', 'kernel32', 'advapi32',
	'shell32']}
