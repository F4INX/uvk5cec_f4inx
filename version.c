
#ifdef VERSION_STRING
	#define VER      VERSION_STRING
#else
	#define VER      ""
#endif

/* Different than Version for compatibility with Chirp, F4INX. */
#ifdef UART_VERSION_STRING
        #define UART_VER UART_VERSION_STRING
#else
        #define UART_VER ""
#endif


const char Version[]      = VER;
const char UARTVersion[]  = UART_VER;

