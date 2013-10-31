from midas import *

lon=np.arange(2.5,360.,5.)
lat=np.arange(-77.5,80.,5.)

X,Y=np.meshgrid(lon,lat)
grid=generic_rectgrid(lon=X,lat=Y,cyclic=False)

S=state(path='http://data.nodc.noaa.gov/thredds/dodsC/woa/WOA09/NetCDFdata/temperature_annual_1deg.nc',fields=['t_an'],z_indices=np.arange(10,11))
S.var_dict['t_an']['Z']=None # Kludge to avoid bug

S.volume_integral('t_an','XY',normalize=True)
sout=np.squeeze(S.t_an[0,0,:])
notes='Original MEAN/MAX/MIN= %(men)4.2f %(min)4.2f %(mx)4.2f'%{'men':sq(S.t_an_xyav.data),'min':sq(np.ma.max(sout)),'mx':sq(np.ma.min(sout))}

T=S.horiz_interp('t_an',target=grid,src_modulo=True,method=1) 
T.volume_integral('t_an','XY',normalize=True)
xax=T.grid.x_T
yax=T.grid.y_T
sout=np.squeeze(T.t_an[0,0,:])

fig,ax=plt.subplots(1)
cf=ax.contourf(xax,yax,sout,np.arange(-2,25,1),extend='both')
plt.colorbar(cf)
ax.grid()
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
zplt=S.var_dict['t_an']['zax_data'][0]

tit='ANN Temperature from NODC WOA09 at Z= %(zplt)s  meters interpolated to 5 deg'%{'zplt':zplt}
notes2='Regridded MEAN/MAX/MIN= %(men)4.2f %(min)4.2f %(mx)4.2f'%{'men':sq(T.t_an_xyav.data),'min':sq(np.ma.max(sout)),'mx':sq(np.ma.min(sout))}

ax.set_title(tit,fontsize=8)

ax.text(0.05,0.95,notes,transform=ax.transAxes,fontsize=8)
ax.text(0.05,0.90,notes2,transform=ax.transAxes,fontsize=8)
plt.show()
