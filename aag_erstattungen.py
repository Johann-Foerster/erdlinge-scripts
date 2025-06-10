from tika import parser
import glob, csv

YEAR = "2024"
ROW_SUM = "Summe"
pdfs = glob.glob(f"aag_erstattungen/{YEAR}/*.pdf")
data = []


def get_pages(filename):
    raw_xml = parser.from_file(pdf, xmlContent=True)
    body = raw_xml["content"].split("<body>")[1].split("</body>")[0]
    body_without_tag = (
        body.replace("<p>", "")
        .replace("</p>", "")
        .replace("<div>", "")
        .replace("</div>", "")
        .replace("<p />", "")
    )
    text_pages = body_without_tag.split("""<div class="page">""")[1:]
    num_pages = len(text_pages)
    if not num_pages == int(
        raw_xml["metadata"]["xmpTPg:NPages"]
    ):  # check if it worked correctly
        print("ERROR in page number crosscheck")
        exit(1)
    return text_pages


def find_index(data, element):
    for index, item in enumerate(data):
        if item == element:
            return index
    return -1


erstattungen_u1 = {}
erstattungen_u2 = {}

for pdf in pdfs:
    text_pages = get_pages(pdf)
    for page in text_pages:
        if "Rückrechnung" in page:
            continue
        lines = page.split("\n")

        vorname = " ".join(
            [
                lines[idx + 2]
                for idx, line in enumerate(lines)
                if "Vorname Rentenversicherungsnummer" in line
            ][0].split(" ")[:-1]
        )
        nachname = " ".join(
            [
                lines[idx + 2]
                for idx, line in enumerate(lines)
                if "Name Pers.Nr." in line
            ][0].split(" ")[:-1]
        )
        name = f"{vorname} {nachname}"

        type = (
            "U1"
            if "Arbeitsunfähigkeit - U1" in page
            else (
                "U2"
                if "Mutterschaft - U2" in page or "Beschäftigungsverbot - U2" in page
                else "TYPE ERROR"
            )
        )
        if type == "TYPE ERROR":
            print("ERROR finding type of page:")
            print(page)

        value = ""
        if "Mutterschaft - U2" in page:
            value = [line for line in lines if " im Monat " in line][0].split(
                " im Monat "
            )[1]
        else:
            value = " ".join(
                [line for line in lines if "Summe Erstattungsbetrag" in line][0].split(
                    " "
                )[2:]
            )
        value_eur = float(value.replace(" €", "").replace(".", "").replace(",", "."))

        if "X Stornierung" in page:
            value_eur = -value_eur
        title = pdf.split("/")[-1].replace(".pdf", "")

        if type == "U1":
            if name not in erstattungen_u1:
                erstattungen_u1[name] = {}
            erstattungen_u1[name][title] = (
                erstattungen_u1[name][title] + value_eur
                if title in erstattungen_u1[name]
                else value_eur
            )
        else:
            if name not in erstattungen_u2:
                erstattungen_u2[name] = {}
            erstattungen_u2[name][title] = (
                erstattungen_u2[name][title] + value_eur
                if title in erstattungen_u2[name]
                else value_eur
            )


def format_float(number):
    integer_part, decimal_part = f"{number:.2f}".split(".")
    return f"{integer_part},{decimal_part}"


# summing up
for name in erstattungen_u1.keys():
    erstattungen_u1[name][ROW_SUM] = sum(erstattungen_u1[name].values())
for name in erstattungen_u2.keys():
    erstattungen_u2[name][ROW_SUM] = sum(erstattungen_u2[name].values())


outfile = f"AAG_Erstattungen_{YEAR}.csv"
titles = [x.split("/")[-1].replace(".pdf", "") for x in pdfs]
print(f"\nWriting {outfile}")

with open(outfile, "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file, delimiter=";")

    writer.writerow(["U1"])
    writer.writerow(["Name"] + titles + [ROW_SUM])
    for name in erstattungen_u1.keys():
        writer.writerow(
            [name]
            + [
                (
                    format_float(erstattungen_u1[name][x])
                    if x in erstattungen_u1[name]
                    else "0"
                )
                for x in titles
            ]
            + [format_float(erstattungen_u1[name][ROW_SUM])]
        )

    writer.writerow([])
    writer.writerow(["U2"])
    writer.writerow(["Name"] + titles + [ROW_SUM])
    for name in erstattungen_u2.keys():
        writer.writerow(
            [name]
            + [
                (
                    format_float(erstattungen_u2[name][x])
                    if x in erstattungen_u2[name]
                    else "0"
                )
                for x in titles
            ]
            + [format_float(erstattungen_u2[name][ROW_SUM])]
        )

print("...written!")
