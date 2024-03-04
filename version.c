#ifdef VERSION_STRING
        const char Version[] = VERSION_STRING;
#else
        const char Version[] = "";
#endif

/* Option to make it different than Version */
/* for compatibility with Chirp, F4INX.     */
#ifdef UART_VERSION_STRING
        const char UARTVersion[] = UART_VERSION_STRING;
#endif
/* Else, #define in version.h */
