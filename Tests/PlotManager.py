import os
from datetime import datetime
from typing import Callable
 
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator 
import numpy as np

class PlotManager:
    """
    Manages matplotlib plots across multiple test files
    """
    def __init__(self):
        self.figure_count = 0
        self.output_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'plots')
        os.makedirs(self.output_dir, exist_ok=True)
        self.current_fig = None
        self.current_ax = None
        self.current_table = None
      
    # Create a new figure and axis  
    def figure(self, figsize=(12, 6)):
        self.figure_count += 1
        self.current_fig = plt.figure(num=self.figure_count, figsize=figsize, clear=True)
        self.current_ax = None
        self.current_table = None
        plt.subplots_adjust(left=0.125, right=0.90, top=0.90, bottom=0.18)
        
        # Force autoscaling
        #self.current_ax.autoscale(enable=True, axis='both', tight=True)
        return 

    def title(self, title, subtitle=None, y_position=0.09):
        """Add a title and optional subtitle to the current figure"""
        self.current_fig.suptitle(title, y=y_position, fontsize=10, fontweight='bold')
        if subtitle:
            self.current_fig.text(0.5, 0.05, subtitle, ha='center', fontsize=8)
            
    # 2D plotting methods
    def axes_limits(self, x_min=None, x_max=None, y_min=None, y_max=None):
        """Explicitly set axis limits, using None for auto values"""
        if self.current_ax is None:
            self.current_ax = plt.gca()
        if self.current_ax:
            if x_min is not None or x_max is not None:
                current_x_min, current_x_max = self.current_ax.get_xlim()
                self.current_ax.set_xlim(
                    x_min if x_min is not None else current_x_min,
                    x_max if x_max is not None else current_x_max
                )
                print(f"X-axis limits set to [{x_min if x_min is not None else current_x_min}, {x_max if x_max is not None else current_x_max}]")
                
            if y_min is not None or y_max is not None:
                current_y_min, current_y_max = self.current_ax.get_ylim()
                self.current_ax.set_ylim(
                    y_min if y_min is not None else current_y_min,
                    y_max if y_max is not None else current_y_max
                )
                print(f"Y-axis limits set to [{y_min if y_min is not None else current_y_min}, {y_max if y_max is not None else current_y_max}]")
        
    def plot(self, x, y, style='b-', linewidth=2, label=None):
        """Plot a line on the current axis"""
        if self.current_ax is None:
            self.current_ax = plt.gca()
        line = self.current_ax.plot(x, y, style, linewidth=linewidth, label=label)
        # Explicitly recalculate the data limits
        self.current_ax.relim()
        self.current_ax.autoscale_view()
        return line

    def scatter(self, x, y, color='r', s=6, label=None):
            """Create a scatter plot on the current axis"""
            return self.current_ax.scatter(x, y, color=color, s=s, label=label)
        
    def bar(self, x, height, width=0.8, **kwargs):
        """Create a bar chart on the current axis"""
        return self.current_ax.bar(x, height, width, fontsize=6, **kwargs)
    
    def vertical_line(self, x, color='g', linestyle='--', alpha=0.5):
        """Add a vertical line at the specified x position"""
        return self.current_ax.axvline(x=x, color=color, linestyle=linestyle, alpha=alpha)
    
    def legend(self, loc='best', fontsize=10, frameon=True, **kwargs):
        """
        Add a legend to the current axis
        
        Args:
            loc: Location of the legend. Options include:
                'best', 'upper right', 'upper left', 'lower left', 
                'lower right', 'center left', 'center right', 
                'lower center', 'upper center', 'center'
            fontsize: Font size for legend text
            frameon: Whether to draw a frame around the legend
            **kwargs: Additional keyword arguments to pass to matplotlib's legend
        
        Returns:
            The Legend object created
        """
        if self.current_ax is None:
            raise ValueError("No current axis available. Create a figure first.")
            
        return self.current_ax.legend(loc=loc, fontsize=fontsize, frameon=frameon, **kwargs) 

    def text(self, x, y, text, **kwargs):
        """Add text at the specified position"""
        return self.current_ax.text(x, y, text, **kwargs)
    
    def xlabel(self, label):
        """Set the x-axis label"""
        self.current_ax.set_xlabel(label)
    
    def ylabel(self, label):
        """Set the y-axis label"""
        self.current_ax.set_ylabel(label)
    
    def xticks(self, ticks=None, labels=None, rotation=0, ha='center'):
        """Set the x-axis ticks and optionally their labels"""
        if ticks is not None:
            self.current_ax.set_xticks(ticks)
        if labels is not None:
            self.current_ax.set_xticklabels(labels, rotation=rotation, ha=ha)
    
    def grid(self, visible=True, axis='both'):
        """Configure the grid"""
        self.current_ax.grid(visible=visible, axis=axis)
    
    # 3D Methods
    def plot_surface(self, x_range, y_range, f : Callable[[float,float], float], style='b-', linewidth=2, label=None):
        """Plot a 3D line on the current axis"""
        if self.current_ax is None:
            self.current_ax = plt.gca()
        
        self.current_ax.clear()  # Clear the current axis for a new plot
        self.current_ax.set_axis_off()  # Hide the axis
        self.current_ax.xaxis.set_visible(False)
        self.current_ax.yaxis.set_visible(False)
        if hasattr(self.current_ax, 'zaxis'):
            self.current_ax.zaxis.set_visible(False)
        self.current_ax.spines['top'].set_visible(False)
        self.current_ax.spines['right'].set_visible(False)
        if hasattr(self.current_ax, 'pane'):
            self.current_ax.xaxis.pane.fill = False
            self.current_ax.xaxis.pane.set_edgecolor('none')
            self.current_ax.yaxis.pane.fill = False
            self.current_ax.yaxis.pane.set_edgecolor('none')
            self.current_ax.zaxis.pane.fill = False
            self.current_ax.zaxis.pane.set_edgecolor('none')
        self.current_ax.grid(False)
        
        x_np = np.array(x_range)
        y_np = np.array(y_range)
        X, Y = np.meshgrid(x_np, y_np)
        Z = np.zeros((len(y_np),len(x_np)))
        for i in range(len(y_np)):
            for j in range(len(x_np)):
                Z[i, j] = f(x_np[j],y_np[i])
        
        self.current_ax = self.current_fig.add_subplot(111, projection='3d')           
        surf = self.current_ax.plot_surface(
            X, Y, Z, 
            cmap = 'viridis',
            linewidth=linewidth,
            antialiased=True
            )
        self.current_ax.view_init(elev=30, azim=45)
        # Explicitly recalculate the data limits
        #self.current_ax.relim()
        #self.current_ax.autoscale_view()
        return surf

    # Table Methods
    def create_table(self, cell_text, col_labels, col_widths=None, fontsize=10, bbox=None,**kwargs):
        """
        Create a standalone table figure without a plot
        
        Args:
            cell_text: 2D list of cell text strings or values
            col_labels: List of column labels
            colWidths: List of column widths as fractions of table width
            fontsize: Base font size for table text
            filename: If provided, save the table to this file
            bbox: Bounding box properties for the table
            **kwargs: Additional keyword arguments for table styling
            
        Returns:
            The Table object created
        """
        try:
            plt.subplots_adjust(left=0.125, right=0.90, top=0.90, bottom=0.07)
            self.current_ax = self.current_fig.add_subplot(111)
            self.current_ax.axis('off')
            
            # Default bounding box for the table
            if bbox is None:
                bbox = [0.1, 0.1, 0.8, 0.8]  # [left, bottom, width, height]
            
            # Create the table
            self.current_table = self.current_ax.table(cellText=cell_text, rowLabels=None, colLabels=col_labels, loc='center', colWidths=col_widths, bbox=bbox, **kwargs)     
            # Style the table
            self.current_table.auto_set_font_size(False)
            self.current_table.set_fontsize(fontsize)
            self.current_table.scale(1.2, 3.5)       
            # Style header row if column labels exist
            if col_labels:
                for j, label in enumerate(col_labels):
                    cell = self.current_table[(0, j)]
                    cell.set_text_props(weight='bold', color='white')
                    cell.set_facecolor('darkblue')        
            # Style row headers if row labels exist
            # if rowLabels:
            #     for i, label in enumerate(rowLabels):
            #         cell = table[(i+1, -1)]
            #         cell.set_text_props(weight='bold')
            #         cell.set_facecolor('lightgray')
            #for (row, col), cell in self.current_table.get_celld().items():
            #    cell.PAD = 0.2
        except Exception as e:
            print(f"Error creating table: {e}")
            self.current_table = None
        return
        
    def style_table_cell(self, row_idx, col_idx, **kwargs):
        """
        Apply styling to a specific table cell
        
        Args:
            table: The table object
            row_idx: Row index (0 is header if colLabels provided)
            col_idx: Column index
            **kwargs: Styling parameters (facecolor, text properties, etc.)
        """
        if self.current_table is None:
            raise ValueError("No current table available. Create a table first.")
        cell = self.current_table[(row_idx, col_idx)]
        
        if 'facecolor' in kwargs:
            cell.set_facecolor(kwargs['facecolor'])
        
        if 'text_props' in kwargs:
            cell.set_text_props(**kwargs['text_props'])
        
        if 'edgecolor' in kwargs:
            cell.set_edgecolor(kwargs['edgecolor'])
            
        if 'linewidth' in kwargs:
            cell._text.set_linespacing(kwargs['linewidth'])        
    
    # Add a timestamp to the current figure
    def timestamp(self, position=(0.95, 0.01)):
        """Add a timestamp to the current figure"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.current_fig.text(position[0], position[1], f"Generated: {timestamp}", 
                    ha='right', fontsize=8, fontstyle='italic')
    
    # Save, Display and Close Methods
    def show(self, filename, wait_for_input=True, block=True):
        """Save the figure to file and optionally display it"""
        if self.current_fig is None:
            raise ValueError("No current figure available. Create a figure first.")
        # Add timestamp before saving
        self.timestamp()        
        # Create full path
        full_path = os.path.join(self.output_dir, filename)
        # Save the figure
        self.current_fig.savefig(full_path)
        print(f"Plot saved as '{full_path}'")
        # Show the plot
        plt.figure(self.current_fig.number)
        plt.draw()
        plt.show(block=block)      
        # Optionally wait for user input
        if wait_for_input and not block:
            user_input = input(f"Figure {self.figure_count} displayed. Press Enter to continue or 'exit' to quit: ")
            if user_input.lower() == 'exit':
                plt.close('all')
                return False
        return True
    
    def close(self):
        """Close all open figures"""
        plt.close('all')
        self.current_fig = None
        self.current_ax = None
        
        
        
        