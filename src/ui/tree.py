#  _______           __ ______ __                __               
# |   |   |.-----.--|  |      |  |--.-----.----.|  |--.-----.----.
# |       ||  _  |  _  |   ---|     |  -__|  __||    <|  -__|   _|
# |__|_|__||_____|_____|______|__|__|_____|____||__|__|_____|__|  

# Re-Usable UI Elements - Treeview Tab

# (c) 2021 JTSage.  MIT License.

import tkinter as Tk
import tkinter.ttk as ttk

class ModCheckTreeTab() :
	"""Build a ttk.TreeView tab	

	Args:
		parent (object): Parent element
		title (str): Title of this tab
		description (str): Description of this tab
		columns (list): Columns for view
		base (object): Root window element
		detail (class): src.ui.detail ModCheckDetailWin or API compatable
		columnExtra (dict, optional): kwargs to each column. Defaults to None.
	"""

	def __init__(self, parent, title, description, columns, base, detail, columnExtra=None) :
		
		self._parent      = parent
		self._UIParts     = {}
		self.title        = title
		self._description = description
		self._base        = base
		self._detailWin   = detail

		self._columns     = [("#"+str(i),j) for i,j in zip(range(1,len(columns)+1), columns)]
		self._columnExtra = columnExtra
		self._isOdd       = True

		self._build()

	def _build(self) :
		""" Build the treeview inside of _parent """
		ttk.Label(self._parent, text=self.title, font='Calibri 12 bold').pack()
		ttk.Label(self._parent, text=self._description, wraplength = 640).pack(fill='x')

		self._UIParts["tree"] = ttk.Treeview(self._parent, selectmode='browse', columns=self._columns, show='headings', style="modCheck.Treeview")
		self._UIParts["tree"].pack(expand=True, side='left', fill='both', pady=(5,0))

		if self._columnExtra is not None :
			for thisExtraKey in self._columnExtra.keys():
				self._UIParts["tree"].column(thisExtraKey, **self._columnExtra[thisExtraKey])

		self._UIParts["VSB"] = ttk.Scrollbar(self._parent, orient="vertical", command=self._UIParts["tree"].yview)
		self._UIParts["VSB"].pack(side='right', fill='y', pady=(25,2))

		self._UIParts["tree"].configure(yscrollcommand=self._UIParts["VSB"].set)

		for col,name in self._columns:
			self._UIParts["tree"].heading(col, text=name, command=lambda _col=col: \
 				 self._treeview_sort(self._UIParts["tree"], _col, False))

		self._UIParts["tree"].bind("<Double-1>", self._on_double_click)

		self._UIParts["tree"].tag_configure('even', background='#E8E8E8')

	def _on_double_click(self, event):
		"""On double-click of a mod, display some information

		Args:
			event (tkinter.Event): The event that just happened (a double click)
		"""
		thisItem    = self._UIParts["tree"].identify('item',event.x,event.y)
		thisModName = self._UIParts["tree"].item(thisItem,"text")

		self._detailWin(
			base     = self._base,
			parent   = self._parent,
			modName  = thisModName,
			modClass = self._base._modList[thisModName]
		)

	def clear_items(self) :
		""" Empty the tree """
		self._UIParts["tree"].delete(*self._UIParts["tree"].get_children())

	def add_item(self, name, values):
		"""Add an item to the tree

		Args:
			name (str): Name column (hidden/descriptor only)
			values (list): Values for shown columns.
		"""

		self._UIParts["tree"].insert(
			parent = '',
			index  = 'end',
			text   = name,
			values = values,
			tags   = ('odd' if self._isOdd else 'even')
		)

		self._isOdd = not self._isOdd

	def _treeview_sort(self, tv, col, reverse):
		""" Sort a tree column numerically or alphabetically

		Args:
			tv (ttk.Treeview): The treeview
			col (str): Column descriptor
			reverse (bool): a->z or z->a (True)
		"""
		l = [(self._size_to_real_num(tv.set(k, col)), k) for k in tv.get_children('')]

		l.sort(
			key=lambda t : self._lower_if_possible(t),
			reverse=reverse
		)		

		# rearrange items in sorted positions
		for index, (val, k) in enumerate(l): # pylint: disable=unused-variable
			tv.item(k, tags= ("even" if ( index % 2 == 0 ) else "odd" ) )
			tv.move(k, '', index)

		# reverse sort next time
		tv.heading(col, command=lambda _col=col: \
				 self._treeview_sort(tv, _col, not reverse))

	def _size_to_real_num(self, text) :
		"""Turn the size column back into a number for sorting

		Args:
			text (str): Human readable file size

		Returns:
			float: File size as an float
		"""
		try :
			num, ext = text.split()

			if ext == "B":
				return float(num)
			if ext == "Kb" :
				return float(num) * 1024
			if ext == "Mb" :
				return float(num) * 1024 * 1024
			if ext == "Gb" :
				return float(num) * 1024 * 1024 * 1024
		
		except ValueError :
			return text

		return text

	def _lower_if_possible(self, x):
		"""Normalize to lowercase for sorting, if possible

		Args:
			x (tuple): Tuple of (text,location) from treeview

		Returns:
			tuple: (text,location) where text is lowercase
		"""
		if isinstance(x[0], float) :
			return x
		else :
			try:
				return (x[0].lower(), x[1])
			except AttributeError:
				return x


	