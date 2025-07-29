import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
from colorama import init, Fore, Style

# Inicializar colorama
init()

def check_lolbas(binary_name):
    """
    Verifica si un binario existe en LOLBAS Project
    Devuelve: (binary_name, found, description_url)
    """
    lolbas_url = "https://lolbas-project.github.io/"
    search_url = f"{lolbas_url}/search?q={binary_name.lower()}"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(search_url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar en todas las tablas
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Saltar encabezados
                    cols = row.find_all('td')
                    if cols:
                        # Comparación flexible (sin .exe y case insensitive)
                        lolbas_bin = cols[0].get_text().strip().lower().replace('.exe', '')
                        current_bin = binary_name.lower().replace('.exe', '')
                        
                        if current_bin == lolbas_bin:
                            link = cols[0].find('a')
                            if link and link.has_attr('href'):
                                description_url = lolbas_url + link['href'].lstrip('/')
                            else:
                                description_url = f"{lolbas_url}#{current_bin}"
                            return (binary_name, True, description_url)
            
            # Búsqueda profunda en el contenido
            clean_bin_name = binary_name.lower().replace('.exe', '')
            if clean_bin_name in response.text.lower():
                # Verificar si es un binario listado (no solo mencionado)
                if f"/#{clean_bin_name}" in response.text.lower():
                    return (binary_name, True, f"{lolbas_url}#{clean_bin_name}")
                
    except requests.exceptions.RequestException as e:
        print(f"{Fore.YELLOW}Error de conexión al verificar {binary_name}: {str(e)}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.YELLOW}Error inesperado al verificar {binary_name}: {str(e)}{Style.RESET_ALL}")
    
    return (binary_name, False, "")

def main():
    print(f"{Style.BRIGHT}=== Verificador de Binarios en LOLBAS ==={Style.RESET_ALL}\n")
    
    # Leer la lista de binarios
    try:
        with open('Only_binaries.txt', 'r') as file:
            binaries = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}Error: No se encontró el archivo 'Only_binaries.txt'{Style.RESET_ALL}")
        return
    except Exception as e:
        print(f"{Fore.RED}Error al leer el archivo: {str(e)}{Style.RESET_ALL}")
        return
    
    if not binaries:
        print(f"{Fore.YELLOW}No se encontraron binarios para verificar{Style.RESET_ALL}")
        return
    
    print(f"Verificando {len(binaries)} binarios en LOLBAS Project...\n")
    
    # Procesamiento paralelo
    found_binaries = []
    not_found_binaries = []
    
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(check_lolbas, binaries))
    except Exception as e:
        print(f"{Fore.RED}Error durante la ejecución paralela: {str(e)}{Style.RESET_ALL}")
        return
    
    # Clasificar resultados
    for binary, found, url in results:
        if found:
            found_binaries.append((binary, url))
        else:
            not_found_binaries.append(binary)
    
    # Mostrar resultados con colores
    print(f"\n{Style.BRIGHT}=== Resultados ==={Style.RESET_ALL}")
    
    print(f"\n{Fore.RED}{Style.BRIGHT}Binarios ENCONTRADOS en LOLBAS ({len(found_binaries)}):{Style.RESET_ALL}")
    for binary, url in found_binaries:
        print(f"{Fore.RED}- {binary}{Style.RESET_ALL} ({url})")
    
    print(f"\n{Fore.BLUE}{Style.BRIGHT}Binarios NO encontrados en LOLBAS ({len(not_found_binaries)}):{Style.RESET_ALL}")
    for binary in not_found_binaries:
        print(f"{Fore.BLUE}- {binary}{Style.RESET_ALL}")
    
    # Verificación de falsos negativos conocidos
    known_lolbins = ['comhost.exe', 'msbuild.exe', 'installutil.exe', 'regsvr32.exe', 
                    'rundll32.exe', 'certutil.exe', 'wmic.exe', 'msiexec.exe',
                    'bitsadmin.exe', 'pcalua.exe', 'forfiles.exe', 'mavinject.exe']
    
    false_negatives = [bin for bin in known_lolbins if bin in not_found_binaries]
    
    if false_negatives:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}¡Advertencia! Los siguientes binarios conocidos aparecen como no encontrados:{Style.RESET_ALL}")
        for bin_name in false_negatives:
            print(f"{Fore.YELLOW}- {bin_name} (verificar manualmente: https://lolbas-project.github.io/#{bin_name.replace('.exe', '')}){Style.RESET_ALL}")
    
    # Guardar resultados
    try:
        with open('found_in_lolbas.txt', 'w') as f:
            f.write("Binario\tURL\n")
            for binary, url in found_binaries:
                f.write(f"{binary}\t{url}\n")
        
        with open('not_found_in_lolbas.txt', 'w') as f:
            for binary in not_found_binaries:
                f.write(f"{binary}\n")
        
        print(f"\n{Style.BRIGHT}Resultados guardados en:{Style.RESET_ALL}")
        print(f"- {Fore.GREEN}found_in_lolbas.txt{Style.RESET_ALL} (binarios encontrados)")
        print(f"- {Fore.GREEN}not_found_in_lolbas.txt{Style.RESET_ALL} (binarios no encontrados)")
    except Exception as e:
        print(f"\n{Fore.RED}Error al guardar los resultados: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
