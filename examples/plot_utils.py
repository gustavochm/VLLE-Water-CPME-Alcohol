import ternary
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def plot_stability(Z_trial):
    npzfile = np.load('stability_3495K.npz')
    Z_test = npzfile['Z_test']
    probably_equilibria = npzfile['probably_equilibria']
    X1, W1, Y1 = npzfile['vlle1']

    fontsize = 12

    width = 3.5
    height = 1. * width
    fig = plt.figure(figsize = (width, height), constrained_layout=True)
    ax = fig.add_subplot(111)

    ax.set_xlabel(r'$\rm x_{water}$', fontsize=fontsize)
    ax.set_ylabel(r'$\rm x_{CPME}$', fontsize=fontsize)
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlim([0,1])
    ax.set_ylim([0,1])

    cp = ax.contourf(Z_test[0], Z_test[1], probably_equilibria, levels=[-1, 0, 1, 2, 3]) 

    trianglex = [X1[0], W1[0], Y1[0], X1[0]]
    triangley = [X1[1], W1[1], Y1[1], X1[1]]
    ax.plot(trianglex, triangley, color='k', alpha=1.0, linestyle='--', marker='s')

    cbar = fig.colorbar(cp, ax=ax)
    cbar.ax.get_yaxis().set_ticks([])
    for j, lab in enumerate(['Bulk \nPhase', 'VLE', 'LLE', 'VLLE']):
        cbar.ax.text(1.5, j - 0.5 , lab, ha='left', va='center', fontsize=fontsize)

    # Plotting Z_trial as a red square
    ax.plot(Z_trial[0], Z_trial[1], marker='s', color='r')
    return fig, ax


def plot_vlle(saft_data, exp_data):
    
    X = saft_data['X']
    W = saft_data['W']
    Y = saft_data['Y']
    T = saft_data['T']
    
    Xexp = exp_data['X']
    Wexp = exp_data['W']
    Yexp = exp_data['Y']
    Texp = exp_data['T']
    
    colorl = 'b'
    colorv = 'r'

    markerX = 's'
    markerW = 'o'
    markerY = 'v'
    fontsize = 12
    markersize = 12
    linewidth = 1.1
    
    
    fig = plt.figure(figsize = (10,5), constrained_layout=True)

    ax3 = fig.add_subplot(121)
    tax = ternary.TernaryAxesSubplot(ax=ax3, scale = 1.0)
    tax.boundary(linewidth=1.0)
    tax.gridlines(color="black", multiple=0.1, linewidth=0.5)

    # SAFT calculations
    tax.plot(X, color = colorl)
    tax.plot(W, color = colorl)
    tax.plot(Y, color = colorv)
    tax.plot([X[0], Y[0], W[0]], linestyle='-', color = 'k', marker='o')
    tax.plot([X[-1], Y[-1], W[-1]], linestyle=':', color = colorl)

    # Experimental data
    tax.scatter(Xexp, color = colorl, marker=markerX, clip_on=False, s=markersize)
    tax.scatter(Wexp, color = colorl, marker=markerW, clip_on=False, s=markersize)
    tax.scatter(Yexp, color = colorv, marker=markerY, clip_on=False, s=markersize)
    # Tie Lines
    nvlle = len(Xexp)
    for i in range(0, nvlle, 1):
        tax.plot([Xexp[i], Yexp[i], Wexp[i]], linestyle=':', color='k', linewidth=linewidth)


    # Set ticks
    tax.ticks(clockwise=True, multiple=0.1, linewidth=1, offset = 0.03,tick_formats='%.1f')

    #Set labels
    tax.right_axis_label(r"$x_{water}\rightarrow$", fontsize=fontsize, offset = 0.15)
    tax.left_axis_label(r"$x_{CPME} \rightarrow$", fontsize=fontsize, offset = 0.15)
    tax.bottom_axis_label(r"$\leftarrow x_{ethanol}$", fontsize=fontsize, offset = 0.15)

    # Remove default Matplotlib Axes
    tax.clear_matplotlib_ticks()
    tax._redraw_labels()
    ternary.plt.axis('off')


    ax = fig.add_subplot(122, projection='3d')

    # SAFT calculations
    ax.plot(X.T[0], X.T[1], T, colorl)
    ax.plot(W.T[0], W.T[1], T, colorl)
    ax.plot(Y.T[0], Y.T[1], T, colorv)

    ax.plot([X[0,0], W[0,0], Y[0,0]], 
            [X[0,1], W[0,1], Y[0,1]], 
            [T[0], T[0], T[0]], 'o-', markersize = 4, color='k')

    ax.plot([X[-1,0], Y[-1,0], W[-1,0]], 
            [X[-1,1], Y[-1,1], W[-1,1]], 
            [T[-1], T[-1], T[-1]], ':', markersize = 4, color=colorl)

    # Experimental data
    ax.scatter(Xexp.T[0], Xexp.T[1], Texp, color=colorl, marker=markerX, s=markersize)
    ax.scatter(Wexp.T[0], Wexp.T[1], Texp, color=colorl, marker=markerW, s=markersize)
    ax.scatter(Yexp.T[0], Yexp.T[1], Texp, color=colorv, marker=markerY, s=markersize)
    # Tie Lines
    for i in range(0, nvlle, 1):
        ax.plot([Xexp[i,0], Yexp[i,0], Wexp[i,0]], 
                [Xexp[i,1], Yexp[i,1], Wexp[i,1]], 
                [Texp[i], Texp[i], Texp[i]], linestyle=':', color='k', linewidth=linewidth)


    ax.set_xlabel(r"$x_{water}, y_{water}$", fontsize = fontsize)
    ax.set_ylabel(r"$x_{CPME}, y_{CPME}$", fontsize = fontsize)
    ax.set_zlabel("T/K", rotation = 90, fontsize = fontsize)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1.])

    ax.view_init(elev=15, azim=-150)
    return fig, ax, tax