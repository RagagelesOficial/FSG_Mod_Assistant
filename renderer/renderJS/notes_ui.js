/*  _______           __ _______               __         __   
   |   |   |.-----.--|  |   _   |.-----.-----.|__|.-----.|  |_ 
   |       ||  _  |  _  |       ||__ --|__ --||  ||__ --||   _|
   |__|_|__||_____|_____|___|___||_____|_____||__||_____||____|
   (c) 2022-present FSG Modding.  MIT License. */

// Folder window UI

/* global l10n, fsgUtil */

/*  __ ____   ______        
   |  |_   | |      |.-----.
   |  |_|  |_|  --  ||     |
   |__|______|______||__|__| */

let thisCollection = null

function processL10N()          { clientGetL10NEntries() }
function clientGetL10NEntries() {
	const l10nSendItems = new Set()

	fsgUtil.query('l10n').forEach((thisL10nItem) => {
		l10nSendItems.add(fsgUtil.getAttribNullError(thisL10nItem, 'name'))
	})

	l10n.getText_send(l10nSendItems)
}

window.l10n.receive('fromMain_getText_return', (data) => {
	fsgUtil.query(`l10n[name="${data[0]}"]`).forEach((item) => { item.innerHTML = data[1] })
})
window.l10n.receive('fromMain_l10n_refresh', () => { processL10N() })

window.mods.receive('fromMain_collectionName', (collection, collectionName, allNotes) => {
	thisCollection = collection
	fsgUtil.byId('collection_name').innerHTML = collectionName

	fsgUtil.query('input').forEach((element) => {
		let thisValue = ''
		if ( typeof allNotes[collection] !== 'undefined' ) {
			thisValue = allNotes[collection][element.id]
		}
		element.value =  ( typeof thisValue !== 'undefined' ) ? thisValue : ''
	})

	processL10N()
})

function clientSetNote(id) {
	const formControl = fsgUtil.byId(id)
	
	window.mods.setNote(id, formControl.value, thisCollection)
}