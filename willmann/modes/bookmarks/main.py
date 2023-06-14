import os
import time
import plyer
import asyncio

from willmann import GenericMode 

from tables.custom import Bookmark

from plugin.utils import register
from plugin.widget import LeftRightEdit
from plugin.widget import InputListStack, InputList

class BookmarkMode(GenericMode):

    def __init__(self, port=None, parent_port=None, config=None):

        super(BookmarkMode, self).__init__(
                 port=port, 
                 parent_port=parent_port, 
                 config=config)

        self.bookmark=Bookmark()
        self.setUI()

    def setUI(self):

        self.ui=InputListStack(item_widget=LeftRightEdit)
        self.ui.main.returnPressed.connect(self.confirm)
        self.ui.main.input.setLabel('Bookmark')

        self.ui.addWidget(InputList(), 'browser')
        self.ui.browser.input.setLabel('Browser')
        self.ui.browser.returnPressed.connect(self.on_browserConfirm)

        self.ui.installEventFilter(self)

    def on_browserConfirm(self):

        item=self.ui.browser.list.currentItem()
        if item: 
            url=self.getUrl(item.itemData['id'])
            self.select(url)

    def deactivate(self):

        self.ui.hide()

    def activate(self):

        self.showMain()

    def toggle(self): 

        if self.ui.isVisible():
            self.deactivate()
        else:
            self.activate()

    @register('b')
    def showBrowserUrls(self): 

        self.update()
        self.ui.show(self.ui.browser)

    @register('m')
    def showMain(self): 

        url=self.getUrl()
        if url:
            self.select(url)
            self.ui.show(self.ui.main)
        else:
            self.showBrowserUrls()

    @register('u')
    def update(self):

        tree=asyncio.run(self.manager.get_tree())
        items=[]
        for window in tree:
            kind=window.ipc_data.get('window_properties', {}).get('class', None)
            if kind in ['qutebrowser', 'Google-chrome']:
                items+=[{'up':window.name, 'id':window.id}]
        self.ui.browser.setList(items)

    def getUrl(self, window_id=None):

        tree=asyncio.run(self.manager.get_tree())
        focused=tree.find_focused()
        workspaces=asyncio.run(self.manager.get_workspaces())
        visible=[w for w in workspaces if w.visible]

        if not window_id: window_id=focused.id
        window=tree.find_by_id(window_id)

        kind=window.ipc_data.get('window_properties', {}).get('class', None)
        if kind in ['qutebrowser', 'Google-chrome']:

            asyncio.run(window.command('focus'))
            os.popen('xdotool key Escape')
            time.sleep(0.1)
            if kind=='Google-chrome':
                os.popen('xdotool key Ctrl+l')
                time.sleep(0.05)
                os.popen('xdotool key Ctrl+c')
                time.sleep(0.05)
            elif kind=='qutebrowser':
                os.popen('xdotool type yy')
                time.sleep(0.05)

            for v in visible:
                asyncio.run(self.manager.command(f'workspace {v.name}'))
            asyncio.run(focused.command('focus'))
            time.sleep(0.05)
            self.ui.show(self.ui.current)
            url=self.clipboard().text()
            return url

    @register('s')
    def select(self, url): 

        data={'url': url, 'kind': 'url'}
        self.bookmark.updateContent(data, summarize=False)
        dlist=[]
        for f in ['title', 'url']:
            dlist+=[{'left':f.title(), 'right':data[f], 'kind':'url'}]
        self.ui.main.setList(dlist)
        self.ui.show(self.ui.main)

    @register('a')
    def confirm(self):

        dlist=self.ui.main.dataList()
        data={}
        for d in dlist:
            if d['left'].lower() in ['title', 'kind', 'url']:
                data[d['left'].lower()]=d['right']
        print(data)
        # self.bookmark.writeRow(data)
        plyer.notification.notify(f'Bookmarked: {data["title"]}', f'{data["url"]}')

if __name__=='__main__':
    app=BookmarkMode(port=33333)
    app.toggle()
    app.run()
