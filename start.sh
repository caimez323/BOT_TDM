# start.sh
git submodule update --init --recursive

cd fonctions/jvaisVX
git checkout tdm
cd ../snifsnouf
git checkout tdm

cd ../..
python app.py
