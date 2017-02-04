# bemto_to_stylus
Sublime Text 3 code converter from pug+bemto to stylus

## Installing
Simple copy the bemto_to_stylus.py in your package folder:
"Sublime Text 3\Packages\User\"

And set the shortcut in key settings:

	{ "keys": ["ctrl+t"], "command": "bemto_to_stylus" },


## Install "bemto"

You must write your pug code in bemto.
More information from bemto: https://github.com/kizu/bemto

Download it, then include main "bemto.pug" file to all your pug files (like mixins):
include ../../../plugins/bemto/bemto


## How its work?

Ok. Now you should typing somethind like this:

	+b.section
		+e.wrapper
			+b.block
				+e.top
					+e.left
						+e.list
							+e.item
								+e.A(href="#").link
							+e.item
								+e.A(href="#").link
							+e.item
								+e.A(href="#").link
					+e.right
						+e.image
							img(src="img/image.png" alt="img")
				+e.bottom
					+b.UL.menu
						+e.LI.item
							+e.A(href="#").link
						+e.LI.item
							+e.A(href="#").link
						+e.LI.item
							+e.A(href="#").link


Copy this text, then go to your stylus file and press the shortcut.
That will be pasted:

	.section
		//
		&__wrapper
			//

	.block
		//
		&__top
			//
		&__left
			//
		&__list
			//
		&__item
			//
		&__link
			//
		&__right
			//
		&__image
			//
		&__bottom
			//

	.menu
		//
		&__item
			//
		&__link
			//




## WIP
I think about mixins dictionary, to auto-paste mixins, like:

	.menu
		ul-reset()
		//
		&__item
			//
		&__link
			+link()
				//
			&:hover
				//

This function named as "autoMixins" in plugin code, and commented now.
