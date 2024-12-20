pkgname=dirfetch
pkgver=1.0.1
pkgrel=1
pkgdesc="A customizable directory-fetching tool like neofetch"
arch=('any')
url="https://github.com/herb-chan/dirfetch"
license=('MIT')
depends=('python' 'python-rich')
makedepends=('python-setuptools' 'python-wheel' 'python-build')

# No source URL or tarball, just use the current directory (assuming you have cloned the repo)
source=()

sha256sums=('SKIP')  # No need for a checksum since we're not fetching a tarball

build() {
  cd "$srcdir/$pkgname-$pkgver"
  python -m venv venv  # Create a virtual environment (optional, for building)
  source venv/bin/activate  # Activate the virtual environment
  pip install setuptools wheel build  # Install the required build tools
  python -m build --wheel  # Build the package into a wheel
}

package() {
  cd "$srcdir/$pkgname-$pkgver"
  source venv/bin/activate  # Activate the virtual environment

  # Install the package directly into the $pkgdir for global installation
  python setup.py install --root="$pkgdir" --optimize=1  # Install the package to the $pkgdir
}
