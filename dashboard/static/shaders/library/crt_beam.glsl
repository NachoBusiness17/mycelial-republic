// CRT Beam Simulator BFI — Blur Busters (Mark Rejhon) & Timothy Lottes
// MIT License — https://www.blurbusters.com/crt — github.com/blurbusters/crt-beam-simulator
// CHAIN ROLE: POST — feed any scene via iChannel0. Needs iFrame, iTimeDelta.
#define MOTION_SPEED 10.0
#define FRAMES_PER_HZ 4.0
#define GAMMA 2.4
#define GAIN_VS_BLUR 0.7
#define SPLITSCREEN 0
#define SPLITSCREEN_X 0.50
#define SPLITSCREEN_Y 0.00
#define SPLITSCREEN_BORDER_PX 2
#define SPLITSCREEN_MATCH_BRIGHTNESS 1
#define FPS_DIVISOR 1.0
#define LCD_ANTI_RETENTION true
#define LCD_INVERSION_COMPENSATION_SLEW 0.001
#define SCAN_DIRECTION 1
#define clampPixel(a) clamp(a, vec3(0.0), vec3(1.0))
float SelF1(float a,float b,bool p){return p?b:a;}
#define IS_INTEGER(x) (floor(x)==x)
#define IS_EVEN_INTEGER(x) (IS_INTEGER(x)&&IS_INTEGER(x/2.0))
float linear2srgb(float c){
    vec3 j=vec3(0.0031308*12.92,12.92,1.0/2.4);
    vec2 k=vec2(1.055,-0.055);
    return clamp(j.x,c*j.y,pow(c,j.z)*k.x+k.y);
}
vec3 linear2srgb(vec3 c){return vec3(linear2srgb(c.r),linear2srgb(c.g),linear2srgb(c.b));}
float srgb2linear(float c){
    vec3 j=vec3(0.04045,1.0/12.92,2.4);
    vec2 k=vec2(1.0/1.055,0.055/1.055);
    return (c>j.x)?pow(c*k.x+k.y,j.z):c*j.y;
}
vec3 srgb2linear(vec3 c){return vec3(srgb2linear(c.r),srgb2linear(c.g),srgb2linear(c.b));}
vec3 getPixelFromOrigFrame(vec2 uv,float getFromHzNumber,float currentHzCounter){
    if(getFromHzNumber>currentHzCounter||getFromHzNumber<currentHzCounter-2.0)return vec3(0.);
    float shiftAmount=10.0/1000.0;
    float baseShift=fract(getFromHzNumber*shiftAmount);
    float px=1.0/iResolution.x;
    uv.x=mod(uv.x+baseShift+px*0.1,1.0)-px*0.1;
    return texture(iChannel0,uv,0.0).rgb;
}
vec3 getPixelFromSimulatedCRT(vec2 uv,float crtRasterPos,float crtHzCounter,float framesPerHz){
    vec3 pixelPrev2=srgb2linear(getPixelFromOrigFrame(uv,crtHzCounter-2.0,crtHzCounter));
    vec3 pixelPrev1=srgb2linear(getPixelFromOrigFrame(uv,crtHzCounter-1.0,crtHzCounter));
    vec3 pixelCurr=srgb2linear(getPixelFromOrigFrame(uv,crtHzCounter,crtHzCounter));
    vec3 result=vec3(0.);
    float brightnessScale=framesPerHz*0.7;
    vec3 colorPrev2=pixelPrev2*brightnessScale;
    vec3 colorPrev1=pixelPrev1*brightnessScale;
    vec3 colorCurr=pixelCurr*brightnessScale;
    float tubePos=1.0-uv.y;
    for(int ch=0;ch<3;ch++){
        float Lprev2=colorPrev2[ch],Lprev1=colorPrev1[ch],Lcurr=colorCurr[ch];
        if(Lprev2<=0.0&&Lprev1<=0.0&&Lcurr<=0.0){result[ch]=0.0;continue;}
        float tubeFrame=tubePos*framesPerHz;
        float fStart=crtRasterPos*framesPerHz;
        float fEnd=fStart+1.0;
        float startPrev2=tubeFrame-framesPerHz;
        float endPrev2=startPrev2+Lprev2;
        float startPrev1=tubeFrame;
        float endPrev1=startPrev1+Lprev1;
        float startCurr=tubeFrame+framesPerHz;
        float endCurr=startCurr+Lcurr;
        #define INTERVAL_OVERLAP(Aa,Ab,Ba,Bb) max(0.0,min(Ab,Ba+1.0)-max(Aa,Ba))
        float o2=max(0.0,min(endPrev2,fEnd)-max(startPrev2,fStart));
        float o1=max(0.0,min(endPrev1,fEnd)-max(startPrev1,fStart));
        float oc=max(0.0,min(endCurr,fEnd)-max(startCurr,fStart));
        result[ch]=o2+o1+oc;
    }
    return linear2srgb(result);
}
void mainImage(out vec4 fragColor,in vec2 fragCoord){
    float effFPH=FRAMES_PER_HZ;
    if(effFPH<2.0)effFPH=100.0;
    vec2 uv=fragCoord/iResolution.xy;
    float effectiveFrame=floor(float(iFrame)*1.0);
    float crtRasterPos=mod(effectiveFrame,effFPH)/effFPH;
    float crtHzCounter=floor(effectiveFrame/effFPH);
    fragColor.rgb=getPixelFromSimulatedCRT(uv,crtRasterPos,crtHzCounter,effFPH);
    fragColor.a=1.0;
}
