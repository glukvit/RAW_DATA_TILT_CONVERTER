#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "jpwin.h"


int rd_win1(char *fname)
{
int j;
FILE *in;
FILE *out;
int sr;
int stfl=0;
char tmp[80];
char sta[8];
char oname[1024];
char ch[8];
char nt[8];
double sr_c;
int slens=3600;
long lbuf[250];
unsigned char *ptr;
unsigned char *ptr_end;
unsigned char *in_data=NULL;
int dec_start[6],dec_now[6],dec_buf[6],
		i,sys_ch0,size;



in=fopen(fname,"rb");
if(!in)return 0;
//RET_RY:
sprintf(oname,"%s.asc",fname);

out=fopen(oname,"w");
if(!out)return 0;



while(1)
{

   if(fread(&size,4,1,in)<=0) 
   {    //  printf("read %s error\n",fname);
	stfl=1;break;
   }
size=mklong((unsigned char*)&size);
//size=swap_4	byte(size);
//printf("in_data: size %d\n", size);


	if((in_data = (unsigned char*)malloc(size* sizeof(unsigned char))) == NULL) 
	{
	stfl=1;	break;
	}
   if(fread(in_data,size-4,1,in)<=0) 
	{
    printf("read %s error\n",fname);
  	 stfl=1;break;
	}


bcd_dec(dec_buf,(char*)in_data);
for(i=0;i<6;i++) dec_start[i]= dec_buf[i];
/*printf("start:%02d%02d%02d %02d%02d%02d\n",
dec_start[0],dec_start[1],dec_start[2],
dec_start[3],dec_start[4],dec_start[5]);
for(i=0;i<6;i++) dec_now[i]=dec_start[i];
*/


ptr=in_data+6;
ptr_end=ptr+size-10;

	while(ptr<ptr_end)
	{

	sys_ch0=0xffff&mkshort(ptr);
//sys_ch0=swap_2byte((unsigned short)sys_ch0);
//	printf("Channel ID= %04X\n",sys_ch0);
	sprintf(sta,"%04X",sys_ch0);
	sr=get_data(&ptr,lbuf,1);
	if(sr)
		{
		for(i=0;i<sr;i++)fprintf(out,"%1d 20%02d-%02d-%02d %02d:%02d:%05.2f %d\n",sys_ch0%10,dec_start[0],dec_start[1],dec_start[2],dec_start[3],dec_start[4],dec_start[5]+i*1./sr,lbuf[i]);
		}

	//if(in_data){free(in_data);in_data=NULL;}
	}	
if(in_data){free(in_data);in_data=NULL;}
}

fclose(in);
fclose(out);
return 0;
}



main(int argc,char *argv[])
{

int i;

if(argc<2)
{
printf("usage: win2asc [winfile]\n");
return 0;
}

for(i=1;i<argc;i++)
rd_win1(argv[i]);

}

