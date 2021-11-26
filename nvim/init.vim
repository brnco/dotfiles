set encoding=utf-8
set number
syntax enable
set noswapfile
set scrolloff=7
set backspace=indent,eol,start
set clipboard+=unnamedplus
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
set autoindent
set fileformat=unix

call plug#begin('~/.config/nvim/plugged')
"Plug 'hzchirs/vim-material'
Plug 'jiangmiao/auto-pairs'
Plug 'scrooloose/nerdtree'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'scrooloose/nerdtree'
Plug 'ryanoasis/vim-devicons'
Plug 'kaicataldo/material.vim', {'branch':'main'}
call plug#end()

let g:material_theme_style='ocean'
set background=dark
colorscheme material

let g:airline_theme='material'

if (has("termguicolors"))
    set termguicolors
endif    
