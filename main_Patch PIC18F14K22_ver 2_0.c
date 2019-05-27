#include <main_Patch PIC18F14K22.h>

#define DRV1        PIN_C3     //DO, H-bridge input
#define DRV2        PIN_C4     //DO, H-bridge input
#define DRV3        PIN_C5     //DO, H-bridge input
#define DRV4        PIN_C6     //DO, H-bridge input
#define ENB_DRVR    PIN_C7     //DO, H-bridge input

int8    Shift;
int16   WaveCntr;

void    Init_IO(void)
{
    output_high(DRV1);  //turn off UL
    output_high(DRV3);  //turn off UR
    output_low(DRV4);   //turn on LL
    output_low(DRV2);   //turn on LR
}


/**
    Waveform to drive 
 **/
 void   WaveForm(void)
{
    //positive phase
    output_low(DRV2);   //turn off LL
    output_high(DRV1);  //turn off UR
    output_low(DRV4);   //turn on UL
    output_high(DRV3);  //turn on LR
    delay_cycles(255);
    
    switch(Shift)   //adjustable mark period
    {
        case 0:
            delay_cycles(41);
            Break;
        case 1:
            delay_cycles(37);
            Break;
        case 2:
            delay_cycles(33);
            Break;
            
        case 3:
            delay_cycles(29);
            Break;
             
        case 4:
            delay_cycles(25);
            Break;
        
        case 5:
            delay_cycles(21);
            Break;
       
        case 6:
            delay_cycles(17);
            Break;

        case 7:
            delay_cycles(13);
            Break;

        case 8:
            delay_cycles(9);
            Break;

         default:
            Break;
    }
    
    // ground bridge outputs
    output_high(DRV4);  //turn off UL
    output_high(DRV1);  //turn off UR
    output_high(DRV2);   //turn on LL
    output_high(DRV3);   //turn on LR
    delay_cycles(48);   //3usec ground
    
    // negative phase
    output_high(DRV2);   //turn off UL
    output_low(DRV3);  //turn off LR
    output_high(DRV2);   //turn on LL
    output_low(DRV1);  //turn on UR
   
    switch(Shift)    //adjustable space period
    {
        case 0:
            delay_cycles(137);
            Break;
        case 1:
            delay_cycles(132);
            Break;
        case 2:
            delay_cycles(127);
            Break;
            
        case 3:
            delay_cycles(122);
            Break;
             
        case 4:
            delay_cycles(117);
            Break;
        
        case 5:
            delay_cycles(112);
            Break;
       
        case 6:
            delay_cycles(107);
            Break;

        case 7:
            delay_cycles(102);
            Break;

        case 8:
            delay_cycles(97);
            Shift = 0;
            Break;

         default:
            Shift = 0;
            Break;
    }
      
     // ground bridge outputs
    output_high(DRV4);  //turn off UL
    output_high(DRV1);  //turn off UR
    output_high(DRV2);   //turn on LL
    output_high(DRV3);   //turn on LR
    delay_cycles(48);   //3usec ground
 
}

void main()
{
      
    setup_timer_1(T1_INTERNAL|T1_DIV_BY_1);        //4.0 ms overflow
    setup_oscillator(OSC_64MHZ);
    Init_IO();
    
    while(TRUE)
    {
        if(!Input(ENB_DRVR))
        {
            WaveCntr++;
            if (WaveCntr > 2000)
            {
                WaveCntr = 0;
                Shift++;
            }
        }
        
        WaveForm();
    }                     

}
