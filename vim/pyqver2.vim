"============================================================================
"File:        pyqver2.vim
"Description: python version checking plugin for syntastic.vim
"Authors:     Adrian Likins <adrian@likins.com>
"
" See https://github.com/alikins/pyqver
"============================================================================

if exists('g:loaded_syntastic_python_pyqver2_checker')
    finish
endif
let g:loaded_syntastic_python_pyqver2_checker = 1

let s:save_cpo = &cpo
set cpo&vim

function! SyntaxCheckers_python_pyqver2_GetLocList() dict
    let makeprg = self.makeprgBuild({})

    let errorformat = '%f:%l: %m'

    let env = syntastic#util#isRunningWindows() ? {} : { 'TERM': 'dumb' }

    let loclist = SyntasticMake({
        \ 'makeprg': makeprg,
        \ 'errorformat': errorformat,
        \ 'env': env })

    return loclist
endfunction


call g:SyntasticRegistry.CreateAndRegisterChecker({
    \ 'filetype': 'python',
    \ 'name': 'pyqver2'})

let &cpo = s:save_cpo
unlet s:save_cpo

" vim: set sw=4 sts=4 et fdm=marker:
