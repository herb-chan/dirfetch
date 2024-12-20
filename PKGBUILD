pkgname=dirfetch
pkgver=1.0.2
pkgrel=1
pkgdesc="A customizable directory-fetching tool like neofetch"
arch=('any')
url="https://github.com/herb-chan/dirfetch"
license=('MIT')
depends=('python' 'python-rich')
makedepends=('python-setuptools' 'python-wheel' 'python-build')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')  # Placeholder for checksum, to be filled automatically by makepkg

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
