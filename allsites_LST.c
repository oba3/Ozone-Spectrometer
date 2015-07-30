#include <stdlib.h>
#include <errno.h>
#include <stdio.h>
#include <sys/uio.h>
#include <math.h>
#include <string.h>
#include <sched.h>
#include <fcntl.h>
#define NDATA 100000

int main(int argc, char *argv[])
{
    char buf[32768];
    char fname[256];
    int line,j,np,yr,dy,hr,mn,sc,mon,qual;
    double vvel,velerr,sum1,sum2,h,dt;
    double plotvel[21], ploterr[21];
    static double tim[NDATA],vel[NDATA],verr[NDATA],wt[NDATA];
    FILE *file1;
    if (argc > 1) sscanf(argv[1], "%s", "data.txt");
    if ((file1 = fopen("data.txt", "r")) == NULL) {
        printf("cannot open file:%s\n", "data.txt");
        return 0;
    }
    line = j = np = 0;
    printf("file %s\n", fname);
    while (fgets(buf, 32768, file1) != 0) {
       if (buf[0] != '*' && buf[0] != '\n') {
//  MIN  HOUR  SEC  DVN2  DAY  VN2  YEAR  MONTH  FPI_DATAQUAL
//       9        22         0     5.27100e-01      19     2.76000e+01    2012        12             2  
            velerr = 0;
            sscanf(buf, "%d %d %d %lf %d %lf %d %d %d",&mn,&hr,&sc,&velerr,&dy,&vvel,&yr,&mon,&qual);
           if(velerr && fabs(vvel) < 200) {
//            printf("%d %d %d %lf %d %lf %d %d %d\n",mn,hr,sc,velerr,dy,vvel,yr,mon,qual);
            vel[j]=vvel; verr[j]=velerr;

            tim[j] = hr+mn/60.0-4.0;  // convert time to Local time
            if(tim[j] > 12) tim[j] += -12;
            j++;
            }
            line++;
      }
     }
    np = j;
    fclose(file1);
    dt = 0.5;
    int i = 0;
    for(h=-5;h<=5;h+=dt){
      vvel = sum1 = 0;
      for(j=0;j<np;j++){ wt[j]=0;
       if(fabs(tim[j] - h) < dt/2.0) {
            vvel += vel[j];
            wt[j]=1;
            sum1++;
        }
       }
       vvel = vvel / sum1;
       sum1 = sum2 = 0;
      for(j=0;j<np;j++){
       if(wt[j]){ // check to see if data is in time range
            sum2 += (vel[j]-vvel)*(vel[j]-vvel);
            sum1++;
        }
       }
     velerr = 3.0*sqrt(sum2/sum1)/sqrt(sum1-1);  // multiplied by 3 to make errors 3 sigma
     printf("hr %4.1f vvel %5.2f err %5.2f num %4.0f\n",h,vvel,velerr,sum1); 
     plotvel[i] = vvel;
     ploterr[i] = velerr;
     i++;
    }

    FILE *f = fopen("out_half.txt", "wb");
    for(int k = 0; k < sizeof(plotvel) / sizeof(plotvel[0]); k++) {
      fprintf(f, "%5.2f\n", plotvel[k]);
    }
    fclose(f);

    FILE *f2 = fopen("out_err_half.txt", "wb");
    for(int k = 0; k < sizeof(ploterr) / sizeof(ploterr[0]); k++) {
      fprintf(f2, "%5.2f\n", ploterr[k]);
    }
    fclose(f2);


    return 0;
}
