# views.py
from flask import Blueprint, render_template, send_from_directory, abort
import os
from ..models.user import User
from ..models.berita import Berita
from ..models.berita_img import Berita_img
from ..models.img import Image
from ..models.akreditasi import Akreditasi
from ..models.dosen import Dosen
from ..models.staff import Staff
from ..models.dokumen import Dokumen
from .documents import UPLOAD_FOLDER

views = Blueprint('views', __name__)


# Beranda
@views.route('/')
def beranda():
    newest_berita = Berita.query.order_by(Berita.date_created.desc()).limit(6).all()

    # Query the database to get the first image associated with each of the newest Berita
    berita_image = [
        Berita_img.query.filter_by(berita_id=berita.berita_id).order_by(Berita_img.id.asc()).first().img_path
        for berita in newest_berita
    ]

    newest_images = Image.query.order_by(Image.id.desc()).limit(3).all()
    carousel_img = [image.img_path for image in newest_images]
    return render_template('home.html', carousel_img=carousel_img, berita_image=berita_image,
                           newest_berita=newest_berita)

@views.route('/berita/<int:berita_id>')
def berita(berita_id):
    # Fetch the Berita from the database based on berita_id
    berita = Berita.query.get(berita_id)

    # Check if the Berita with the given ID exists
    if not berita:
        abort(404)  # Return a 404 Not Found error if the Berita doesn't exist

    return render_template('berita.html', berita=berita)

# Profil Fakultas
@views.route('/profil/akreditasi')
def akreditasi():
    # Assuming Akreditasi has a 'departemen' column to distinguish different departments
    departemen_list = ['Teknik Komputer', 'Sistem Informasi', 'Informatika']  # Modify with your actual departemen names

    akreditasi_data = {}
    for departemen in departemen_list:
        akreditasi_data[departemen] = Akreditasi.query.filter_by(departemen=departemen).all()

    return render_template('akreditasi.html', akreditasi_data=akreditasi_data)


@views.route('/profil/akreditasi/download/<int:akreditasi_id>')
def download_akreditasi(akreditasi_id):
    # Fetch the Dokumen instance from the database
    document = Akreditasi.query.get_or_404(akreditasi_id)

    # Return the file for download
    return send_from_directory(UPLOAD_FOLDER, os.path.basename(document.dokumen_path), as_attachment=True)


@views.route('/profil/struktur-organisasi')
def organisasi():
    # Fetch data for Fakultas leaders
    # Assuming 'Dekan', 'Wakil Dekan I', 'Wakil Dekan II', 'Wakil Dekan III' are the roles for faculty leaders
    fakultas_leaders = Dosen.query.filter(
        Dosen.jabatan.in_(['Dekan', 'Wakil Dekan I', 'Wakil Dekan II', 'Wakil Dekan III'])
    ).all()

    # Assigning unique IDs based on the order of roles
    role_id_mapping = {
        'Dekan': 1,
        'Wakil Dekan I': 2,
        'Wakil Dekan II': 3,
        'Wakil Dekan III': 4
    }

    for dosen in fakultas_leaders:
        dosen.id = role_id_mapping.get(dosen.jabatan, 0)

    # Fetch data for department leaders
    department_leaders = Dosen.query.filter_by(jabatan='Kepala Departemen').all()

    department_mapping = {
        'Teknik Komputer': 1,
        'Sistem Informasi': 2,
        'Informatika': 3
    }
    for dosen in department_leaders:
        dosen.id = department_mapping.get(dosen.departemen, 0)

    # Fetch data for lab heads
    lab_heads = Dosen.query.filter_by(jabatan='Kepala Laboratorium').all()

    # Fetch data for quality assurance body
    quality_assurance_body = Dosen.query.filter_by(jabatan='Ketua Penjaminan Mutu').all()

    # Fetch data for departement quality assurance body
    departement_quality_assurance_body = Dosen.query.filter_by(jabatan='Ketua Kendali Mutu Departemen').all()

    # Fetch data for administrative staff
    kepala_kantor = Staff.query.filter_by(jabatan='Kepala Kantor').first()
    kasi_admin_umum = Staff.query.filter_by(jabatan='Kasi Administrasi dan Umum').first()
    kasi_keuangan_aset = Staff.query.filter_by(jabatan='Kasi Keuangan dan Aset').first()

    # Render the template with the fetched data
    return render_template('organisasi.html',
                           fakultas_leaders=fakultas_leaders,
                           department_leaders=department_leaders,
                           lab_heads=lab_heads,
                           quality_assurance_body=quality_assurance_body,
                           departement_quality_assurance_body=departement_quality_assurance_body,
                           kepala_kantor=kepala_kantor,
                           kasi_admin_umum=kasi_admin_umum,
                           kasi_keuangan_aset=kasi_keuangan_aset)


@views.route('/profil/staff-dosen')
def dosen():
    # Fetch Dosen records where jabatan is not null (excluding null roles like 'Dekan', 'Wakil Dekan I', etc.)
    dosen_list = Dosen.query.filter(Dosen.departemen.isnot(None)).all()

    # Pass the dosen_list to the template
    return render_template('dosen.html', dosen_list=dosen_list)


# Adjust the route to fetch all Staff records
@views.route('profil/staff-kependidikan')
def tendik():
    staff_list = Staff.query.all()
    return render_template('tendik.html', staff_list=staff_list)


@views.route('profil/visi-misi')
def visi_misi():
    return render_template('visi-misi.html')


@views.route('profil/tujuan')
def tujuan():
    return render_template('tujuan.html')


@views.route('profil/senat')
def senat():
    return render_template('coming-soon.html')


# Kendali Mutu
@views.route('penjaminan-mutu/profil')
def bapem_profil():
    return render_template('profil-bapem.html')


@views.route('penjaminan-mutu/struktur')
def bapem_struktur():
    # Fetch data for quality assurance body
    quality_assurance_body = Dosen.query.filter(
        Dosen.jabatan.in_(['Ketua Penjaminan Mutu', 'Sekertaris Penjaminan Mutu'])).all()

    # Fetch data for department quality assurance body
    departement_quality_assurance_body = Dosen.query.filter(
        Dosen.jabatan.in_(['Ketua Kendali Mutu Departemen', 'Anggota Kendali Mutu Departemen'])).all()

    return render_template('struktur-bapem.html', quality_assurance_body=quality_assurance_body,
                           departement_quality_assurance_body=departement_quality_assurance_body)


@views.route('penjaminan-mutu/dokumen-sop')
def bapem_dokumen():
    # Fetch documents labeled as SOP
    sop_documents = Dokumen.query.filter_by(dokumen_label='sop').all()

    return render_template('dokumen_bapem.html', sop_documents=sop_documents)
