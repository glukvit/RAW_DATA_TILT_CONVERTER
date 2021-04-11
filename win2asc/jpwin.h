#define long int
int mklong(unsigned char *ptr)
        
        {
        unsigned char *ptr1;
        unsigned long a;
        ptr1=(unsigned char *)&a;
        *ptr1++=*(ptr+3);
        *ptr1++=*(ptr+2);
        *ptr1++=*(ptr+1);
        *ptr1  =*(ptr);
        return a;
        }

short mkshort(unsigned char *ptr)
        
        {
        unsigned char *ptr1;
        short a;
        ptr1=(unsigned char *)&a;
        *ptr1++=*(ptr+1);
        *ptr1  =*(ptr);
        return a;
        }




void bcd_dec(int *dest, char *sour)

		{
	int cntr;
	for(cntr=0;cntr<6;cntr++)
		dest[cntr]=((sour[cntr]>>4)&0xf)*10+(sour[cntr]&0xf);
	}



int time_cmp(int *t1,int *t2)
	{
	int cntr;
	for(cntr=0;cntr<6;cntr++)
		{
	printf("time_cmp: %2d t1 = %2d t2 = %2d\n", cntr, t1[cntr], t2[cntr]);
		if(t1[cntr]>t2[cntr]) return 1;
		if(t1[cntr]<t2[cntr]) return -1;
		}
	return 0;
	}

int get_data(unsigned char **dp,long *buf,int idx)



{
	unsigned char *ddp;
	 int gh,s_rate,g_size,sys_ch0,i,b_size;
	ddp=(*dp);
	gh=mklong(ddp);
//	gh=swap_4byte(gh);
	s_rate=gh&0xfff;
	
	ddp+=4;
	if(b_size=(gh>>12)&0xf) g_size=b_size*(s_rate-1)+4;
	else g_size=(s_rate>>1)+4;
	*dp+=4+g_size;
	sys_ch0=gh>>16;
	if(idx==0) return(s_rate);

	/* read group */
	buf[0]=mklong(ddp);
	ddp+=4;
	switch(b_size)
		{
		case 0:
			for(i=1;i<s_rate;i+=2)
				{
				buf[i]=buf[i-1]+((*(char *)ddp)>>4);
				buf[i+1]=buf[i]+(((char)(*(ddp++)<<4))>>4);
				}
			break;
		case 1:
			for(i=1;i<s_rate;i++)
				buf[i]=buf[i-1]+(*(char *)(ddp++));
			break;
		case 2:
			for(i=1;i<s_rate;i++)
				{
				buf[i]=buf[i-1]+mkshort(ddp);
				ddp+=2;
				}
			break;
		case 3:
			for(i=1;i<s_rate;i++)
				{
				buf[i]=buf[i-1]+(mklong(ddp)>>8);
				ddp+=3;
				}
			break;
		case 4:
			for(i=1;i<s_rate;i++)
				{
				buf[i]=buf[i-1]+mklong(ddp);
				ddp+=4;
				}
			break;
		default:
			return(-1);	/* bad header */
		}
	return(s_rate);	/* normal return */
}

