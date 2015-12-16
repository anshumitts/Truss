import math
import pygame
import pprint
import numpy as np
import sys
from pygame.locals import *
import matplotlib.pyplot as plt
import Tkinter as tk
import scipy.io
import locale
import os
locale.setlocale( locale.LC_ALL, "")

nodes=[];
members=[];
def rnd(x,y=0):
	return round(x,y);
#from win32api import GetSystemMetrics
sw = 640;
sh = 480;
sz = 90;
txt= 20;
max_y=480;
f=0.05;

window=pygame.display.set_mode((sw,sh));
canvas1=pygame.Rect(0,0,sw-100,sh)
show=window.subsurface(canvas1);
canvas2=pygame.Rect(sw-100,0,100,sh)
side=window.subsurface(canvas2);
canvas3=pygame.Rect(sw/2-150,sh/2-150,200,70)
popup=window.subsurface(canvas3);

popup_rect=pygame.Rect(0,0,200,70)


surface_joint_arr=[[-1 for x in range(640)] for j in range(480)];
memberid=0;
nodeid=0;
#first screen
button_truss       = pygame.Rect((10,20),(sz,20))
button_details     = pygame.Rect((10,50),(sz,20))
button_force       = pygame.Rect((10,80),(sz,20))
button_calculate   = pygame.Rect((10,110),(sz,20))




button_X       = pygame.Rect((20,40),(40,20))
button_Y       = pygame.Rect((80,40),(40,20))
button_R       = pygame.Rect((140,40),(40,20))


button_truss_start       = pygame.Rect((10,20),(sz,20))
button_truss_end       = pygame.Rect((10,50),(sz,20))
#bottom_butt
button_back = pygame.Rect((10,440),(sz,20))

#second screen
button_polynomial = pygame.Rect((10,20),(sz,20))
button_linear     = pygame.Rect((10,50),(sz,20))

#menu_load
button_pointl     = pygame.Rect((10,20),(sz,20))
button_pointc     = pygame.Rect((10,50),(sz,20))

#menu_udl
button_udlp     = pygame.Rect((10,20),(sz,20))
button_udll     = pygame.Rect((10,50),(sz,20))

#menu_support
button_hinge = pygame.Rect((10,20),(sz,20)) #2
button_fixed = pygame.Rect((10,50),(sz,20)) #1
button_shre  = pygame.Rect((10,80),(sz,20)) #4
button_inhi  = pygame.Rect((10,110),(sz,20)) #3


blk=(0,0,0)
w=(255,255,255)
li=(24, 4, 255)
ml=(100,255,60)
blu=(62, 49, 117)
RED=(163, 32, 8)
GRN=(45, 134, 51)
org=(255,140,0)

green=(0,255,0)
button=(143, 141, 155)
wit=(255,255,255)
load_col=(235,14,14)
udl_col=(0,0,0)
udl_top_col=(238, 0, 135)
pdl_rec=(238, 0, 135)
ldl_col=(255, 111, 0)
col=(0,0,0)
ld_rec=(255, 225, 0)

window.fill(blk);
show.fill(wit);
side.fill(blu);

pi=math.pi;
sqt=math.sqrt;
cosi=math.cos;
sine=math.sin;
atan=math.atan2;
local=[[1,-1],[-1,1]];
mininf= -1*float("inf");

pygame.init()

def arrow_beam((f,x,y,r)):
	r=-1*r;
	radar = (x,y)
	k=0;
	if(f>0):
		k=-0.7;
	elif(k<=0):
		k=+0.7;

	radar_len = 10
	x1=radar[0] + math.cos(r)*radar_len;
	y1=radar[1] + math.sin(r)*radar_len;
	x2=radar[0] - math.cos(r)*radar_len;
	y2=radar[1] - math.sin(r)*radar_len;
	print (x1,y1,x2,y2)
	pygame.draw.line(show,org ,(x1,y1),(x2,y2) , 2)
	pygame.draw.line(show,org ,(x1,y1),(x1 - k*math.cos(r+pi/6)*radar_len, y1 - k*math.sin(r+pi/6)*radar_len),2)
	pygame.draw.line(show,org ,(x1,y1),(x1 - k*math.cos(r-pi/6)*radar_len, y1 - k*math.sin(r-pi/6)*radar_len),2)
	pygame.draw.line(show,org ,(x2,y2),(x2 + k*math.cos(r-pi/6)*radar_len, y2 + k*math.sin(r-pi/6)*radar_len),2)
	pygame.draw.line(show,org ,(x2,y2),(x2 + k*math.cos(r+pi/6)*radar_len, y2 + k*math.sin(r+pi/6)*radar_len),2)
	pygame.display.flip();
	texts(rnd(f,2),x,y,(127,255,0))

def confirm(tempi,temp_joint,temp_member,temp_nodeid,tem_memid):
        t=True
        global nodeid, memberid
        button_conf = pygame.Rect((470,450),(70,20))
        pygame.draw.rect (show, GRN, button_conf)
        text_load('Confirm',480,465)
        button_nconf = pygame.Rect((390,450),(70,20))
        pygame.draw.rect (window, RED, button_nconf)
        text_load('Cancel',400,465)
        pygame.display.flip()
        while t:
                for event in pygame.event.get():
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        
                        ## if mouse is pressed get position of cursor ##
                        pos = pygame.mouse.get_pos()
                        ## check if cursor is on button ##
                        if button_conf.collidepoint(pos):
                        	for x in temp_joint:
                        		nodes.append(x);
                        	for y in temp_member:
                        		members.append(y);
                        	temp_joint=[];
                        	temp_member=[];
                        	nodeid=temp_nodeid;
                        	memberid=tem_memid;
                        	temp_nodeid=0;
                        	tem_memid=0;
                        	return(1,tempi)
                        elif button_nconf.collidepoint(pos):
                    		temp_joint=[];
                        	temp_member=[];
                        	temp_nodeid=0;
                        	tem_memid=0;
                        	return (0,0)

def confirm_rotate(tempi,temp_screen,ri,r):
        t=True
        global nodeid, memberid
        button_conf = pygame.Rect((470,450),(70,20))
        pygame.draw.rect (show, GRN, button_conf)
        text_load('Confirm',480,465)
        button_nconf = pygame.Rect((390,450),(70,20))
        pygame.draw.rect (window, RED, button_nconf)
        text_load('Cancel',400,465)
        pygame.display.flip()
        while t:
                for event in pygame.event.get():
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        
                        ## if mouse is pressed get position of cursor ##
                        pos = pygame.mouse.get_pos()
                        ## check if cursor is on button ##
                        if button_conf.collidepoint(pos):
                        	return(r,tempi)
                        elif button_nconf.collidepoint(pos):
                        	return (ri,temp_screen)




def texts(txt,x,y,col=ml):
   font=pygame.font.Font(None,20)
   wrtxt=font.render(str(txt), 1,col)
   show.blit(wrtxt, (x, y))

def details_n(txt,x,y,col=ml):
   font=pygame.font.Font(None,20)
   wrtxt=font.render(str(txt), 1,col)
   popup.blit(wrtxt, (x, y))

def texts_butt(txt,x,y):
   font=pygame.font.Font(None,20)
   wrtxt=font.render(str(txt), 1,wit)
   side.blit(wrtxt, (x, y))

def text_load(txt,x,y,col=blk):
   font=pygame.font.Font(None,20)
   wrtxt=font.render(str(txt), 1,blk)
   show.blit(wrtxt, (x-2, int(y-10)))

def wrt_file():
        scipy.io.savemat(path_file, mdict={'Top': top,'Bottom': bottom,'ludl': udl_line,'pudl': udl_poly,'pt_load':load_pt,'support': support})

def back_butt((xq,yq)):
        pygame.draw.rect (side, button, button_back)
def circle(x,y,r=5,tk=3):
	pygame.draw.circle(show, RED, (x,y), r, tk)
	pygame.display.flip()

def map_y(((xi,yi), (xf,yf))):
	return ((xi,-1*yi+max_y),(xf,-1*yf+max_y));

class member:
	def __init__(self, ((xi,yi), (xf,yf)),i_d,E,A,nid1,nid2,m1,m2,f):
		self.id=i_d
		self.xi=xi;
		self.yi=yi;
		self.xf=xf;
		self.yf=yf;
		self.l=sqt((rnd(f*(xf))-rnd(f*xi))*(rnd(f*(xf))-rnd(f*xi))+(rnd(f*(yf))-rnd(f*(yi)))*(rnd(f*(yf))-rnd(f*(yi))));
		self.E=E;
		self.A=A;
		self.nid1=nid1;
		self.nid2=nid2;
		self.m1=m1;
		self.m2=m2
		self.m=atan(rnd(f*(yf))-rnd(f*(yi)),rnd(f*(xf))-rnd(f*xi));
		self.force_x=0;
		self.force_y=0;
	def roataion_angle(self,nodes):
		self.m1=nodes[self.nid1].nodal_plain();
		self.m2=nodes[self.nid2].nodal_plain();

	def matrix_local(self,matrix_global,EA):
		l=self.l;
		m=self.m;
		m1=self.m1;
		m2=self.m2;
		nid1=self.nid1;
		nid2=self.nid2;
		print m,m1,m2,l,"\n"
		i=0;
		f=EA/l;
		self.local_mat=[[f*cosi(m-m1)*cosi(m-m1),f*cosi(m-m1)*sine(m-m1),-1*f*cosi(m-m2)*cosi(m-m1),-1*f*cosi(m-m1)*sine(m-m2)],
						[f*cosi(m-m1)*sine(m-m1),f*sine(m-m1)*sine(m-m1),-1*f*cosi(m-m2)*sine(m-m1),-1*f*sine(m-m1)*sine(m-m2)],
						[-1*f*cosi(m-m1)*cosi(m-m2),-1*f*cosi(m-m2)*sine(m-m1),f*cosi(m-m2)*cosi(m-m2),f*cosi(m-m2)*sine(m-m2)],
						[-1*f*cosi(m-m1)*sine(m-m2),-1*f*sine(m-m2)*sine(m-m1),f*cosi(m-m2)*sine(m-m2),f*sine(m-m2)*sine(m-m2)]];
		print_arr(self.local_mat);
		matrix_global[nid1*2+0][nid1*2+0]+=self.local_mat[0][0];
		matrix_global[nid1*2+0][nid1*2+1]+=self.local_mat[0][1];
		matrix_global[nid1*2+0][nid2*2+0]+=self.local_mat[0][2];
		matrix_global[nid1*2+0][nid2*2+1]+=self.local_mat[0][3];
		matrix_global[nid1*2+1][nid1*2+0]+=self.local_mat[1][0];
		matrix_global[nid1*2+1][nid1*2+1]+=self.local_mat[1][1];
		matrix_global[nid1*2+1][nid2*2+0]+=self.local_mat[1][2];
		matrix_global[nid1*2+1][nid2*2+1]+=self.local_mat[1][3];
		matrix_global[nid2*2+0][nid1*2+0]+=self.local_mat[2][0];
		matrix_global[nid2*2+0][nid1*2+1]+=self.local_mat[2][1];
		matrix_global[nid2*2+0][nid2*2+0]+=self.local_mat[2][2];
		matrix_global[nid2*2+0][nid2*2+1]+=self.local_mat[2][3];
		matrix_global[nid2*2+1][nid1*2+0]+=self.local_mat[3][0];
		matrix_global[nid2*2+1][nid1*2+1]+=self.local_mat[3][1];
		matrix_global[nid2*2+1][nid2*2+0]+=self.local_mat[3][2];
		matrix_global[nid2*2+1][nid2*2+1]+=self.local_mat[3][3];
		return matrix_global;

	def ass_force(self,nodes):
		(nid1_x,nid1_y,m1,(x1,y1))=nodes[self.nid1].strain_give();
		(nid2_x,nid2_y,m2,(x2,y2))=nodes[self.nid2].strain_give();
		m=self.m;
		E=self.E;
		A=self.A;
		l=self.l;
		dx=(nid1_x*cosi(m-m1)+nid1_y*sine(m-m1))-(nid2_x*cosi(m-m2)+nid2_y*sine(m-m2))
		new_l=sqt(((nid1_x*cosi(m1)-dx*cosi(m)-nid2_x*cosi(m2))*(nid1_x*cosi(m1)-dx*cosi(m)-nid2_x*cosi(m2)))+((nid1_y*sine(m2)-dx*sine(m)-nid2_y*sine(m2))*(nid1_y*sine(m2)-dx*sine(m)-nid2_y*sine(m2))))
		if(new_l>l):
			self.force=((E*A*(dx)/l));
		else:
			self.force=(E*A*dx/l);
		return(self.force,(x1+x2)/2,(y1+y2)/2,m)


class node:
	def __init__(self,i_d,x=0,y=0,m=0):
		self.id=i_d;
		self.force_x=0;
		self.force_y=0;
		self.dis_x=0;
		self.dis_y=0;
		self.xc=x;
		self.yc=y;
		self.m=m;
		self.x=1;
		self.y=1;
		self.fd_x=0;
		self.fd_y=0;
	def force(self,x,y):
		m=self.m;
		self.force_x=x*cosi(m)+y*sine(m);
		self.force_y=y*cosi(m)-x*sine(m);
	def oforce_x(self):
		return self.force_x*self.x;
	def oforce_y(self):
		return self.force_y*self.y;
	def disp_x(self):
		return self.dis_x;
	def disp_y(self):
		return self.dis_y;
	def cond_strain(self,x,y):
		self.x=x;
		self.y=y;
	def ret_const(self):
		return(self.x,self.y)
	def id_give(self):
		return self.id;
	def rotate(self,m):
		self.m=m;
	def coor_give(self):
		return (self.xc,self.yc);
	def nodal_plain(self):
		return self.m;
	def strain_give(self):
		return (self.fd_x,self.fd_y,self.m,self.coor_give());
		




def print_arr(matrix_global):
	for x in matrix_global:
		if(type(x) is list):
			for y in x :
				print (str(float("{0:.5f}".format(y)))),;
		else:
			print (str(float("{0:.5f}".format(x))));
		print "\n";

def print_multi_arr(arrays):
	for z in arrays:
		print_arr(z);
		print "\n";


def matrix_shift(matrix_global,size,frm,to):
	temp=matrix_global[to];
	matrix_global[to]=matrix_global[frm];
	matrix_global[frm]=temp;
	i=0;
	temp=None;
	while(i<2*size):
		temp=matrix_global[i][frm];
		matrix_global[i][frm]=matrix_global[i][to];
		matrix_global[i][to]=temp;
		i=i+1;
	return matrix_global;


def forceAndDisp_matrix_create(joints,length):
	temp=[];
	displ=[];
	disp=[];
	id_mat=[];
	i=0;
	while(i<length):
		temp.append(joints[i].oforce_x());
		temp.append(joints[i].oforce_y());
		displ.append(joints[i].x);
		displ.append(joints[i].y);
		disp.append(joints[i].dis_x);
		disp.append(joints[i].dis_y);
		id_mat.append(i+0.1);
		id_mat.append(i+0.2);
		i=i+1;
	return (temp,id_mat,displ,disp);

def swap(a,b):
	return(b,a);

def split_matrix(force_mat,displ_mat,matrix_global,disp_mat,size):
	leng=sum(displ_mat);
	Qk =[force_mat[i] for i in range(leng)];
	Duk=[displ_mat[i]for i in range(leng)];
	Quk=[force_mat[leng+i] for i in range(size-leng)];
	Dk =[disp_mat[i] for i in range(size-leng)];
	k11=[[matrix_global[j][i] for i in range(leng)] for j in range(leng)];
	k12=[[matrix_global[j][leng+i] for i in range(size-leng)] for j in range(leng)]
	k21=[[matrix_global[leng+j][i] for i in range(leng)] for j in range(size-leng)]
	k22=[[matrix_global[leng+j][leng+i] for i in range(size-leng)] for j in range(size-leng)]
	return k11,k12,k21,k22,Qk,Quk,Duk,Dk;
def sort_force_mat(force_mat,id_mat,displ_mat,matrix_global,disp_mat,size):
	i=0;
	while i<size:
		y=i;
		while y<size:
			if(displ_mat[y]>displ_mat[i]):
				(force_mat[y],force_mat[i])=swap(force_mat[y],force_mat[i]);
				(id_mat[y],id_mat[i])=swap(id_mat[y],id_mat[i]);
				(displ_mat[y],displ_mat[i])=swap(displ_mat[y],displ_mat[i]);
				(disp_mat[y],disp_mat[i])=swap(disp_mat[y],disp_mat[i]);
				matrix_shift(matrix_global,size/2,y,i);
			y=y+1;
		i=i+1;
	return(force_mat,id_mat,displ_mat,matrix_global,disp_mat);

def matrix_multiply(a,b):
	return np.dot(a,b);
def matrix_subtract(a,b):
	return np.subtract(a,b);

def inverse_mat(x):
	return np.linalg.inv(x);

def assign(Duk,Dk,id_mat):
	global nodes;
	t=0;
	while(t<len(Duk)):
		index=int(id_mat[t]);
		check=id_mat[t]-index
		if(str(check) == str(0.1)):
			nodes[index].fd_x=Duk[t];
		if(str(check) == str(0.2)):
			nodes[index].fd_y=Duk[t];
		t=t+1;
	k=0;
	while(k<len(Dk)):
		index=int(id_mat[t+k]);
		if(str(id_mat[t+k]-index)==str(0.1)):
			nodes[index].fd_x=Dk[k];
		if(str(id_mat[t+k]-index)==str(0.2)):
			nodes[index].fd_y=Dk[k];
		k=k+1;
	for x in members:
		arrow_beam(x.ass_force(nodes));
		print x.id,x.force,
global EA_ini;
def Value_EA():
    global EA_ini;
    def send():
            global EA_ini
            EA_ini = mainTextBox.get()
            onClick()

    def onClick():
            root.destroy()
    root = tk.Tk()
    mainLabel = tk.Label(root, text='enter EA value ')
    mainLabel.pack()
    mainTextBox=tk.Entry(root)
    mainTextBox.pack()
    mySubmitButton = tk.Button(root, text='Submit', command=send)
    mySubmitButton.pack()
    quit = tk.Button(root, text=' Quit ', command=onClick)
    quit.pack()
    root.mainloop()
    return EA_ini

def main():
	length=len(nodes);
	print length
	EA_mem=Value_EA();
	matrix_global=[[0 for i in range(2*length)] for j in range(2*length)];
	for x in members:
		x.roataion_angle(nodes);
		x.matrix_local(matrix_global,int(EA_mem));		
	print_arr(matrix_global);
	(force_mat,id_mat,displ_mat,disp_mat)=forceAndDisp_matrix_create(nodes,length);
	(force_mat,id_mat,displ_mat,matrix_global,disp_mat)=sort_force_mat(force_mat,id_mat,displ_mat,matrix_global,disp_mat,2*length);
	print_multi_arr((force_mat,id_mat,displ_mat,matrix_global,disp_mat));
	(k11,k12,k21,k22,Qk,Quk,Duk,Dk)=(split_matrix(force_mat,displ_mat,matrix_global,disp_mat,2*length));
	print_multi_arr((k11,k12,k21,k22,Qk,Quk,Duk,Dk))
	Duk=(matrix_multiply(inverse_mat(k11),matrix_subtract(Qk,matrix_multiply(k12,Dk))));
	print Duk,id_mat;
	assign(Duk,Dk,id_mat);
	for x in members:
		print x.force


def surface_value(arr,a,x,y):
	for i in range(x-4,x+4):
		for j in range(y-4,y+4):
			if(j>0 and j<480):
				if(i>0 and i<540):
					arr[i][j]=a;
	return arr;

def draw_arc((xi,yi),m):
	{
	pygame.draw.arc(show, RED, (xi,yi,6,6), 0, m, 3)
	}
def angles(x,y):
	if(x>y):
		return(x,y);
	else:return(y,x);
def member_make(temp_nodeid,node_ini,(xi,yi),temp_surface,temp_screen,tem_memid,temp_joint):
	temp_member=[];
	temp=temp_screen;
	global nodeid,memberid;
	print nodeid,memberid,tem_memid,temp_nodeid;
	l=True
	while l:
		show.blit(temp_screen,(0,0))
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit();
			if event.type== pygame.MOUSEMOTION:
				(xt,yt)=pygame.mouse.get_pos()
				if(temp_surface[xt][yt]==-1):
					pygame.draw.line(show,(blu),(xi,yi),(xt,yt),3)
					texts((rnd(f*xt),rnd(f*(-1*yt+max_y))),xt,yt,blk);
					circle(xt,yt)
				else:
					node_val=(temp_surface[xt][yt]);
					if (node_val>=nodeid):
						index=node_val-nodeid
						(xt,yt)=temp_joint[index].coor_give();
					else:
						(xt,yt)=nodes[node_val].coor_give();
					if(xt!=xi):
						pygame.draw.line(show,(blu),(xi,yi),(xt,yt),3)
				(m1,m2)=angles(atan(-(yt-yi),(xt-xi)),0);
				pygame.draw.arc(show, (blk), (xi-25, yi-25, 50, 50), m2,m1 , 1)
				texts(atan(-(yt-yi),(xt-xi))*180/pi,xi,yi);
				pygame.display.flip();
			if event.type== pygame.MOUSEBUTTONDOWN:
				if(pygame.mouse.get_pressed()[2]):
					show.blit(temp_screen,(0,0))
					l=False
				else:
					(xt,yt)=pygame.mouse.get_pos()
					if(temp_surface[xt][yt]==-1):
						pygame.draw.line(show,(blu),(xi,yi),(xt,yt),3)
						circle(xt,yt)
						texts((rnd(f*xt),rnd(f*(-1*yt+max_y))),xt,yt,blk);
						temp_member.append(member(map_y(((xi,yi),(xt,yt))),tem_memid,1,1,node_ini,temp_nodeid,0,0,f));
						temp_joint.append(node(temp_nodeid,xt,yt,0));
						temp_surface=surface_value(temp_surface,temp_nodeid,xt,yt);
						temp_nodeid=temp_nodeid+1;
						tem_memid=tem_memid+1;
						node_ini=temp_nodeid-1;
					else:
						node_val=(temp_surface[xt][yt]);
						if (node_val>=nodeid):
							index=node_val-nodeid
							(xt,yt)=temp_joint[index].coor_give();
						else:
							(xt,yt)=nodes[node_val].coor_give();
						if(xt!=xi):
							pygame.draw.line(show,(blu),(xi,yi),(xt,yt),3)
							temp_member.append(member(map_y(((xi,yi),(xt,yt))),tem_memid,1,1,node_ini,node_val,0,0,f));
							tem_memid=tem_memid+1;
							node_ini=node_val;
						pygame.display.flip();
					(xi,yi)=(xt,yt);

					temp_screen=show.copy();
	(r,temp)=confirm(temp_screen,temp_joint,temp_member,temp_nodeid,tem_memid);
	temp_member=[]
	return(r,temp)



def menu_truss():
	side.fill(blu);
	temp_joint=[];
	global nodeid, memberid,surface_joint_arr;
	pygame.display.flip();
	temp_screen=show.copy();
	temp_surface=[[surface_joint_arr[j][i] for i in range(640)] for j in range(480)];
	k=True;
	while k:
		temp_nodeid=nodeid;
		show.blit(temp_screen,(0,0))
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit();
			if event.type== pygame.MOUSEMOTION:
				(xt,yt)=pygame.mouse.get_pos()
				texts((rnd(f*xt),rnd(f*(-1*yt+max_y))),xt,yt,blk);
				circle(xt,yt)
			if event.type== pygame.MOUSEBUTTONDOWN:
				if(pygame.mouse.get_pressed()[2]):
					show.blit(temp_screen,(0,0))
					k=False
				else:
					(xt,yt) = pygame.mouse.get_pos()
					if(temp_surface[xt][yt]==-1):
						circle(xt,yt);
						temp_surface=surface_value(temp_surface,temp_nodeid,xt,yt)
						temp_joint.append(node(temp_nodeid,xt,yt,0));
						temp_nodeid=temp_nodeid+1;
						texts((rnd(f*xt),rnd(f*(-1*yt+max_y))),xt,yt,blk);
						temp=show.copy()
						(r,temp)=member_make(temp_nodeid,temp_nodeid-1,(xt,yt),temp_surface,temp,memberid,temp_joint)
					else:
						node_val=(temp_surface[xt][yt]);
						if (node_val>=nodeid):
							index=node_val-nodeid
							(xt,yt)=temp_joint[index].coor_give();
						else:
							(xt,yt)=nodes[node_val].coor_give();
						temp=show.copy()
						(r,temp)=member_make(temp_nodeid,node_val,(xt,yt),temp_surface,temp,memberid,temp_joint)
					if(r):
						show.blit(temp,(0,0));
						temp_screen=show.copy();
					else:
						show.blit(temp_screen,(0,0));
					temp_joint=[];
					temp_screen=show.copy()
		surface_joint_arr=temp_surface;
        pygame.display.flip();
                        ## check if cursor is on button ##

color=[blk,RED]

def make_popup(x,y,r,node_val):
	pygame.draw.rect (popup, GRN, popup_rect);
	details_n("Node ID: "+str(node_val),10,2,wit);
	pygame.draw.rect (popup,color[x],button_X);
	pygame.draw.rect (popup,color[y],button_Y);
	pygame.draw.rect (popup,RED,button_R);
	details_n("resisX",21,20,wit)
	details_n("resisY",81,20,wit)
	details_n("Rot: "+str(r),141,20,wit)

def line_draw(x1,y1,r):
	radar = (x1,y1)
	print (x1,y1)
	radar_len = 20
	pygame.draw.line(show, Color("black"),(radar[0] + math.cos(r)*radar_len,radar[1] + math.sin(r)*radar_len) ,(radar[0] - math.cos(r)*radar_len,radar[1] - math.sin(r)*radar_len) , 1)
	pygame.display.flip();

def rotate(temp_screen,x,y,ri):
	k=True;
	temp=temp_screen;
	while k:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit();
			if event.type==pygame.MOUSEMOTION:
				(xt,yt) = pygame.mouse.get_pos()
				show.blit(temp_screen,(0,0));
				r=atan(rnd(f*(yt))-rnd(f*(y)),rnd(f*(xt))-rnd(f*x))
				print r;
				line_draw(x,y,r);
				pygame.display.flip();
			if event.type== pygame.MOUSEBUTTONDOWN:
				if(pygame.mouse.get_pressed()[2]):
					show.blit(temp,(0,0))
					pygame.display.flip();
					k=False
			else:		
					(xt,yt) = pygame.mouse.get_pos()
					show.blit(temp_screen,(0,0));
					r=-1*atan(rnd(f*(yt))-rnd(f*(y)),rnd(f*(xt))-rnd(f*x))
					line_draw(x,y,-1*r);
					(m1,m2)=angles(r,0);
					pygame.draw.arc(show, (blk), (x-25, y-25, 50, 50), m2,m1 , 1)
					temp=show.copy();
					texts(r,x,y-100);
					pygame.display.flip();
	if(r<0):
		r=pi+r;
	else:
		r=r;
	return confirm_rotate(temp,temp_screen,ri,r)

def details_nodes((xti,yti),node_val):
	global nodes;
	print "in"
	(x,y)=nodes[node_val].ret_const();
	r=nodes[node_val].nodal_plain();
	temp_screen=show.copy();
	temp=temp_screen
	make_popup(x,y,r,node_val);
	pygame.display.flip()
	k=True;
	while k:
		temp_nodeid=nodeid;
		show.blit(temp,(0,0))
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit();
			if event.type== pygame.MOUSEBUTTONDOWN:
				if(pygame.mouse.get_pressed()[2]):
					show.blit(temp,(0,0))
					pygame.display.flip();
					k=False
				else:		
					(xt,yt) = pygame.mouse.get_pos()
					if(button_X.collidepoint((xt-(sw/2-150),yt-(sh/2-150)))):
						if(x):
							x=0;
						else:
							x=1;
						make_popup(x,y,r,node_val)
						pygame.display.flip();
					if(button_Y.collidepoint((xt-(sw/2-150),yt-(sh/2-150)))):
						if(y):
							y=0;
						else:
							y=1;
						make_popup(x,y,r,node_val)
						pygame.display.flip();
					if(button_R.collidepoint((xt-(sw/2-150),yt-(sh/2-150)))):
						(r,temp)=rotate(temp_screen,xti,yti,r)
						show.blit(temp,(0,0))
						make_popup(x,y,r,node_val)
						pygame.display.flip();
	return ((x,y),r)
first_time=True;
def menu_frame():
	global surface_joint_arr, first_time;
	temp_surface=[[surface_joint_arr[j][i] for i in range(640)] for j in range(480)];
	temp_screen=show.copy();
	i=0;
	if(first_time):
		first_time=False;
		while(i<len(nodes)):
			nodes[i].cond_strain(1,1);
			nodes[i].rotate(0);
			i=i+1
	k=True;
	while k:
		temp_nodeid=nodeid;
		show.blit(temp_screen,(0,0))
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit();
			if event.type== pygame.MOUSEBUTTONDOWN:
				if(pygame.mouse.get_pressed()[2]):
					show.blit(temp_screen,(0,0))
					k=False
				else:		
					(xt,yt) = pygame.mouse.get_pos()
					if(temp_surface[xt][yt]==-1):
						continue;
					else:
						node_val=(temp_surface[xt][yt]);
						(xt,yt)=nodes[node_val].coor_give();
						((x,y),m)=details_nodes((xt,yt),node_val);
						temp_screen=show.copy();
						nodes[node_val].cond_strain(x,y);
						nodes[node_val].rotate(m);

def line_draw_arrow(x,y,r):
	radar = (x,y)
	radar_len = 20
	pygame.draw.line(show, Color("black"),(radar[0] + math.cos(r)*radar_len,radar[1] + math.sin(r)*radar_len) ,(x,y) , 2)
	pygame.draw.line(show,Color("black"),(radar[0] + math.cos(r)*radar_len,radar[1] + math.sin(r)*radar_len),(radar[0] + math.cos(r+pi/2)*radar_len,radar[1] + math.sin(r+pi/2)*radar_len),2)
	pygame.draw.line(show,Color("black"),(radar[0] + math.cos(r)*radar_len,radar[1] + math.sin(r)*radar_len),(radar[0] + math.cos(r-pi/2)*radar_len,radar[1] + math.sin(r-pi/2)*radar_len),2)
	pygame.display.flip();
value=0
def force_input():
    global value;
    def send():
            global value
            value = mainTextBox.get()
            onClick()

    def onClick():
            root.destroy()
    root = tk.Tk()
    mainLabel = tk.Label(root, text='enter load value ')
    mainLabel.pack()
    mainTextBox=tk.Entry(root)
    mainTextBox.pack()
    mySubmitButton = tk.Button(root, text='Submit', command=send)
    mySubmitButton.pack()
    quit = tk.Button(root, text=' Quit ', command=onClick)
    quit.pack()
    root.mainloop()
    return value

def force_nodes((x,y),node_val):
	global nodes;
	temp_screen=show.copy();
	temp=temp_screen
	pygame.display.flip()
	k=True;
	while k:
		temp_nodeid=nodeid;
		show.blit(temp,(0,0))
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit();
			if event.type==pygame.MOUSEMOTION:
				(xt,yt) = pygame.mouse.get_pos()
				show.blit(temp_screen,(0,0));
				r=atan(rnd(f*(yt))-rnd(f*(y)),rnd(f*(xt))-rnd(f*x))
				line_draw_arrow(x,y,r);
				(m1,m2)=angles(-1*r,0);
				pygame.draw.arc(show, (blk), (x-25, y-25, 50, 50), m2,m1 , 1)
				temp=show.copy();
				texts(-1*r,x,y-100);
			if event.type== pygame.MOUSEBUTTONDOWN:
				if(pygame.mouse.get_pressed()[2]):
					show.blit(temp_screen,(0,0))
					pygame.display.flip();
					k=False
				else:		
					(xt,yt) = pygame.mouse.get_pos()
					show.blit(temp_screen,(0,0));
					r=atan(rnd(f*(yt))-rnd(f*(y)),rnd(f*(xt))-rnd(f*x))
					line_draw_arrow(x,y,r);
					(m1,m2)=angles(-1*r,0);
					pygame.draw.arc(show, (blk), (x-25, y-25, 50, 50), m2,m1 , 1)
					force=force_input();
					temp=show.copy();
					texts(-1*r,x,y-100);
					(re,tmep)=confirm_rotate(temp,temp_screen,0,force)
					if(re):
						show.blit(tmep,(0,0));
						pygame.display.flip();
						return (int(force)*cosi(-1*r),int(force)*sine(-1*r))
					else:
						continue;
			pygame.display.flip();
					

def menu_load():
	global surface_joint_arr, first_time;
	temp_surface=[[surface_joint_arr[j][i] for i in range(640)] for j in range(480)];
	temp_screen=show.copy();
	i=0;
	if(first_time):
		first_time=False;
		while(i<len(nodes)):
			nodes[i].cond_strain(1,1);
			nodes[i].rotate(0);
			i=i+1
	k=True;
	while k:
		temp_nodeid=nodeid;
		show.blit(temp_screen,(0,0))
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit();
			if event.type== pygame.MOUSEBUTTONDOWN:
				if(pygame.mouse.get_pressed()[2]):
					show.blit(temp_screen,(0,0))
					k=False
				else:		
					(xt,yt) = pygame.mouse.get_pos()
					if(temp_surface[xt][yt]==-1):
						continue;
					else:
						node_val=(temp_surface[xt][yt]);
						(xt,yt)=nodes[node_val].coor_give();
						(fx,fy)=force_nodes((xt,yt),node_val);
						print (fx,fy)
						temp_screen=show.copy();
						nodes[node_val].force(fx,fy);


def display_side_menu():
	side.fill(blu);
	pygame.draw.rect (side, button, button_truss)
	pygame.draw.rect (side, button, button_details)
	pygame.draw.rect (side, button, button_force)
	pygame.draw.rect (side, button, button_calculate)
	texts_butt("Make",txt,22)
	texts_butt("Details",txt,52)
	texts_butt("Force",txt,82)
	texts_butt("Calc",txt,112)
	pygame.display.flip()
    

def screen_main():
	pygame.display.flip()
	temp=window.copy();
	display_side_menu();
	pygame.display.flip()
	while True:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                    	pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        
                        ## if mouse is pressed get position of cursor ##
                        pos = pygame.mouse.get_pos()
                        (xt,yt)=pos
                        ## check if cursor is on button ##
                        if button_truss.collidepoint((xt-540,yt-0)):
                                menu_truss()
                                display_side_menu();
                        elif button_details.collidepoint((xt-540,yt-0)):
                                menu_frame()
                                display_side_menu();
                        elif button_force.collidepoint((xt-540,yt-0)):
                                menu_load()
                                display_side_menu();
                        elif button_calculate.collidepoint((xt-540,yt-0)):
                                main();
                                display_side_menu();

screen_main();