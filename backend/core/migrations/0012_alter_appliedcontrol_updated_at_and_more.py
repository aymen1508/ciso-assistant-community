# Generated by Django 5.0.4 on 2024-05-03 12:41
# loadedlibrary updates added manually

import django.db.models.deletion
import iam.models
import uuid
from django.db import migrations, models

BUILTIN_LIBRARY_URNS = set(
    [
        "urn:intuitem:risk:library:nis2-directive",
        "urn:intuitem:risk:library:cmmc-2.0",
        "urn:intuitem:risk:library:pcidss-4_0",
        "urn:intuitem:risk:library:nist-ssdf-1.1",
        "urn:intuitem:risk:library:rgs-v2.0",
        "urn:intuitem:risk:library:doc-pol",
        "urn:intuitem:risk:library:dora",
        "urn:intuitem:risk:library:3cf-v2",
        "urn:intuitem:risk:library:owasp-top-10-web",
        "urn:intuitem:risk:library:hds-v2023-a",
        "urn:ackwa:risk:library:pgssi-s-1.0",
        "urn:intuitem:risk:library:gdpr-checklist",
        "urn:intuitem:risk:library:anssi-guide-hygiene",
        "urn:intuitem:risk:library:iso27001-2022",
        "urn:intuitem:risk:library:mitre-attack-v14",
        "urn:protocolpaladin:risk:library:matrice-des-risques-critiques-5x5",
        "urn:intuitem:risk:library:risk-matrix-3x3-mult",
        "urn:intuitem:risk:library:fedramp-rev5",
        "urn:intuitem:risk:library:nist-csf-1.1",
        "urn:intuitem:risk:library:critical_risk_matrix_3x3",
        "urn:intuitem:risk:library:nist-800-171-rev2",
        "urn:intuitem:risk:library:ecc-1",
        "urn:intuitem:risk:library:secnumcloud-3.2-annexe-2",
        "urn:intuitem:risk:library:secnumcloud-3.2",
        "urn:intuitem:risk:library:3cf-ed1-v1",
        "urn:intuitem:risk:library:fadp",
        "urn:intuitem:risk:library:tisax-v6.0.2",
        "urn:intuitem:risk:library:owasp-asvs-4.0.3",
        "urn:protocolpaladin:risk:library:anssi-recommandations-configuration-systeme-gnu-linux",
        "urn:intuitem:risk:library:lpm-oiv-2019",
        "urn:intuitem:risk:library:aircyber-v1.5.2",
        "urn:intuitem:risk:library:nist-ai-rmf-1.0",
        "urn:intuitem:risk:library:dfs-500-2023-11",
        "urn:intuitem:risk:library:nist-csf-2.0",
        "urn:intuitem:risk:library:anssi-nis-rules",
        "urn:intuitem:risk:library:risk-matrix-5x5-sensitive",
        "urn:intuitem:risk:library:iso27001-2022-fr",
        "urn:intuitem:risk:library:pspf",
        "urn:intuitem:risk:library:nist-privacy-1.0",
        "urn:intuitem:risk:library:ccb-cff-2023-03-01",
        "urn:intuitem:risk:library:cra-proposal-annexes",
        "urn:ackwa:risk:library:risk-matrix-4x4-pgssi-s-1.0",
        "urn:intuitem:risk:library:essential-eight",
        "urn:intuitem:risk:library:nist-sp-800-66-rev2",
        "urn:intuitem:risk:library:critical_risk_matrix_5x5",
        "urn:protocolpaladin:risk:library:matrice-des-risques-critiques-3x3",
        "urn:intuitem:risk:library:nist-sp-800-53-rev5",
        "urn:intuitem:risk:library:tiber-eu-2018",
        "urn:intuitem:risk:library:anssi-genai-security-recommendations-1.0",
        "urn:intuitem:risk:library:soc2-2017",
    ]
)


def adapt_libraries(apps, schema_editor):
    LoadedLibrary = apps.get_model("core", "LoadedLibrary")
    for library in LoadedLibrary.objects.all():
        library.builtin = (
            library.urn in BUILTIN_LIBRARY_URNS
        )  # There is no perfect way to verify is a loaded custom library is builtin or not
        # There is no way to generate the objects_meta dictionary without reading all files from ./backend/library/libraries, but we can generate the missing objects_meta values at the same time we generate the StoredLibrary objects.

        library.objects_meta = {
            "frameworks": library.frameworks.count(),
            "threats": library.threats.count(),
            "reference_controls": library.reference_controls.count(),
            "risk_matrix": library.risk_matrices.count(),
        }
        library.save()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_auto_20240501_1342"),
        ("iam", "0003_alter_folder_updated_at_alter_role_updated_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appliedcontrol",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
        migrations.AlterField(
            model_name="asset",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
        migrations.AlterField(
            model_name="complianceassessment",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
        migrations.AlterField(
            model_name="evidence",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
        migrations.AlterField(
            model_name="framework",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
        migrations.AlterField(
            model_name="project",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
        migrations.AlterField(
            model_name="referencecontrol",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
        migrations.AlterField(
            model_name="requirementassessment",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
        migrations.AlterField(
            model_name="requirementnode",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
        migrations.AlterField(
            model_name="riskacceptance",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
        migrations.AlterField(
            model_name="riskassessment",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
        migrations.AlterField(
            model_name="riskmatrix",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
        migrations.AlterField(
            model_name="riskscenario",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
        migrations.AlterField(
            model_name="threat",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
        migrations.RenameModel("Library", "LoadedLibrary"),
        migrations.AlterField(
            model_name="loadedlibrary",
            name="provider",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Provider"
            ),
        ),
        migrations.AlterField(
            model_name="loadedlibrary",
            name="urn",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="URN"
            ),
        ),
        migrations.AlterField(
            model_name="loadedlibrary",
            name="dependencies",
            field=models.ManyToManyField(
                blank=True, to="core.loadedlibrary", verbose_name="Dependencies"
            ),
        ),
        migrations.AddField(
            model_name="loadedlibrary",
            name="builtin",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="loadedlibrary",
            name="objects_meta",
            field=models.JSONField(default=dict),
        ),
        migrations.AlterModelOptions(
            name="loadedlibrary",
            options={
                "abstract": False,
                "unique_together": {("urn", "locale", "version")},
            },
        ),
        migrations.AlterField(
            model_name="framework",
            name="library",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="frameworks",
                to="core.loadedlibrary",
            ),
        ),
        migrations.AlterField(
            model_name="referencecontrol",
            name="library",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reference_controls",
                to="core.loadedlibrary",
            ),
        ),
        migrations.AlterField(
            model_name="riskmatrix",
            name="library",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="risk_matrices",
                to="core.loadedlibrary",
            ),
        ),
        migrations.AlterField(
            model_name="threat",
            name="library",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="threats",
                to="core.loadedlibrary",
            ),
        ),
        migrations.CreateModel(
            name="StoredLibrary",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                (
                    "is_published",
                    models.BooleanField(default=False, verbose_name="published"),
                ),
                (
                    "ref_id",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Reference ID",
                    ),
                ),
                (
                    "locale",
                    models.CharField(
                        default="en", max_length=100, verbose_name="Locale"
                    ),
                ),
                (
                    "default_locale",
                    models.BooleanField(default=True, verbose_name="Default locale"),
                ),
                (
                    "provider",
                    models.CharField(
                        blank=True, max_length=200, null=True, verbose_name="Provider"
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=200, null=True, verbose_name="Name"),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "annotation",
                    models.TextField(blank=True, null=True, verbose_name="Annotation"),
                ),
                (
                    "urn",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="URN"
                    ),
                ),
                (
                    "copyright",
                    models.CharField(
                        blank=True, max_length=4096, null=True, verbose_name="Copyright"
                    ),
                ),
                ("version", models.IntegerField(verbose_name="Version")),
                (
                    "packager",
                    models.CharField(
                        blank=True,
                        help_text="Packager of the library",
                        max_length=100,
                        null=True,
                        verbose_name="Packager",
                    ),
                ),
                ("builtin", models.BooleanField(default=False)),
                ("objects_meta", models.JSONField()),
                ("dependencies", models.JSONField(null=True)),
                ("is_loaded", models.BooleanField(default=False)),
                ("hash_checksum", models.CharField(max_length=64)),
                ("content", models.TextField()),
                (
                    "folder",
                    models.ForeignKey(
                        default=iam.models.Folder.get_root_folder,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_folder",
                        to="iam.folder",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "unique_together": {("urn", "locale", "version")},
            },
        ),
        migrations.RunPython(adapt_libraries),
    ]
