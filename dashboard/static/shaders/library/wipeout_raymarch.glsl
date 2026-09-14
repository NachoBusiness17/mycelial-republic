// Raymarched wipeout racer — bpm clock — operator-supplied (adapted, ES3)
// CHAIN ROLE: SCENE. iChannel0 = heightfield/music texture.
float bpm;
vec3 ro,rt,rd,rp,rs,x,y,z;
mat3 o;
float speed;
vec3 hp;
vec3 hash3d(vec3 p){
     uvec3 q=floatBitsToUint(p);
     q=((q>>16u)^q.yzx)*1111111111u;
     q=((q>>16u)^q.yzx)*1111111111u;
     q=((q>>16u)^q.yzx)*1111111111u;
     return vec3(q)/float(-1u);
}
struct GS{vec3 hash,cell,size;};
struct Grid{GS sub;float d;};
Grid grid;
#define gsub grid.sub
void dosub(vec3 p){
     gsub.size=vec3(.5);
     for(int i=0;i<5;i++){
        gsub.cell=(floor(p/gsub.size)+.5)*gsub.size;
        gsub.cell.y=0.;
        gsub.hash=hash3d(gsub.cell);
        if(i==4||gsub.hash.x<.5)break;
        gsub.size*=.5;
     }
}
void dogrid(vec3 ro,vec3 rd){
     dosub(ro+rd*.001);
     vec3 src=-(ro-gsub.cell)/rd;
     src+=abs(.5*gsub.size/rd);
     grid.d=min(src.x,min(src.z,src.z));
}
vec3 stepNoise(float x,float n){
    float u=smoothstep(.5-n,.5+n,fract(x));
    return mix(hash3d(vec3(floor(x),-1.,11111.)),hash3d(vec3(floor(x+1.),-1.,11111.)),u);
}
vec3 path(vec3 p){
    vec3 o=vec3(0.);
    o.x+=sin(p.z*.1);
    o.y+=cos(p.z*.1)*2.;
    o.y+=sin(p.z*.5)*.2;
    o.x+=cos(p.z*.2)*.5;
    o.xy+=(stepNoise(p.z*.15,.3).xy-.5);
    o+=cross(sin(p*.3),cos(p*.4))*.1;
    return o;
}
float sdChamferBox(vec2 p,vec2 b,float chamfer){
    p=abs(p)-b;
    p=(p.y>p.x)?p.yx:p.xy;
    p.y+=chamfer;
    const float k=1.0-sqrt(2.0);
    if(p.y<0.0&&p.y+p.x*k<0.0)return p.x;
    if(p.x<p.y)return (p.x+p.y)*sqrt(0.5);
    return length(p);
}
vec3 erot(vec3 p,vec3 ax,float t){return mix(dot(ax,p)*ax,p,cos(t))+cross(ax,p)*sin(t);}
float box(vec3 p,vec3 b){p=abs(p)-b;return length(max(vec3(0),p))+min(0.,max(p.x,max(p.y,p.z)));}
vec2 sdf(vec3 p){
    vec2 h;
    hp=p;
    vec3 off=path(p);
    hp+=off;
    h.x=sdChamferBox(hp.xy,vec2(1.,.5),.3);
    h.x=max(hp.y,abs(h.x)-.1);
    h.y=1.;
    vec2 t;
    vec3 tp=p;
    t.x=dot(tp,vec3(0,1,0))-hash3d(vec3(floor(p.xz*.01),floor(uSeed))).x*2.0;
    t.x=max(-(abs(p.x)-2.1),t.x);
    t.y=0.;
    h=t.x<h.x?t:h;
    tp=p;tp+=off;tp.y+=.1;tp.z-=speed;
    tp=erot(tp,normalize(vec3(0,.0,1)),sin(off.x));
    tp.x=abs(tp.x)-.125;
    tp=erot(tp,normalize(vec3(0,.1,1)),.785);
    t.x=box(tp,vec3(.25,.015,.65));
    t.y=-0.;
    h=t.x<h.x?t:h;
    tp+=(cross(sin(hp*7.),cos(hp.yzx*5.))*mix(.01,.1,tp.z/2.));
    t.x=max(tp.z,length(tp.xy)-.02+mix(.01,.03,tp.z/2.));
    t.y=10.;
    h=t.x<h.x?t:h;
    tp=p-gsub.cell;
    t.x=box(tp,vec3(.49,10.49*gsub.hash.y,.49)*gsub.size);
    t.x=max(-(abs(p.x)-2.1),t.x);
    t.y=-1.;
    h=t.x<h.x?t:h;
    return h;
}
#define q(s) s*sdf(p+s).x
vec3 norm(vec3 p,float ee){vec2 e=vec2(-ee,ee);return normalize(q(e.xyy)+q(e.yxy)+q(e.yyx)+q(e.xxx));}
void mainImage(out vec4 fragColor,in vec2 fragCoord){
    bpm=uBPM*iTime/60.;
    speed=bpm*(1.+uEnergy*.8);
    vec2 uv=(fragCoord-.5*iResolution.xy)/iResolution.y;
    vec3 col=vec3(0.);
    vec3 rnd=hash3d(vec3(fragCoord.xy,bpm));
    vec3 trnd=stepNoise(bpm*.125,.1+(rnd.x-.5)*.1);
    speed*=2.;
    ro=vec3(0.,.1,-.5-trnd.x),rt=vec3(0);
    ro.z+=speed;ro-=path(ro);
    rt.z+=speed;rt-=path(rt);
    z=normalize(rt-ro),x=vec3(z.z,0.,-z.x);
    rd=(o=mat3(x,cross(z,x),z))*normalize(rs=vec3(uv,.5-mix(.4,.1,trnd.x+rnd.y*.03)));
    rp=ro;
    vec3 light=vec3(1.,2.,-3.)+ro;
    vec3 acc=vec3(0.);
    vec2 d=vec2(1.);
    float rl=0.,glen=0.;
    for(float i=0.;i++<200.;){
        if(glen<=rl){dogrid(rp,rd);glen+=grid.d;}
        d=sdf(rp);
        if(d.y==10.){acc+=vec3(.1,.2,.3)*exp(-abs(d.x))/(10.-9.*exp(-3.*fract(rp.z*.1)));d.x=max(.001,abs(d.x));}
        if(d.x<.001)break;
        rl=min(rl+d.x,glen);
        rp=ro+rd*rl;
    }
    if(d.x<.001){
        vec3 n=norm(rp,.001);
        vec3 ld=normalize(light-rp);
        float dif=max(0.,dot(ld,n));
        float spc=pow(max(0.,dot(reflect(ld,n),rd)),32.);
        float fre=pow(1.+dot(rd,n),4.);
        if(d.y==1.){
            col=mix(vec3(.5+.25*mod(floor(hp.x*5.)+floor(hp.z*5.),2.))*dif+spc,col,fre);
            if(mod(floor(hp.z/4.),8.)==0.)col=.1/col;
        }else if(d.y==0.){col=mix(vec3(.1)*dif+spc,col,fre);}
        else{col=mix(vec3(exp(-5.*fract(gsub.hash.z+bpm)))*dif+spc,col,fre);}
    }
    col=mix(col,vec3(.01),1.-exp(-.001*rl*rl*rl));
    col=sqrt(col+acc);
    col=mix(col,fwidth(sqrt(col)*10.)*vec3(.9,.3,.1),trnd.z+uv.y);
    col+=vec3(.91,.71,.35)*uBass*.12;
    fragColor=vec4(col,1);
}
