/**
 * Diccionario de regiones y sus comnunas
 */
var comunas = {
    "Arica y Parinacota" : ["Arica", "Camarones", "General Lagos", "Putre"],
    "Tarapacá" : ["Alto Hospicio", "Iquique", "Camiña", "Colchane", "Huara", "Pica","Pozo Almonte"],
    "Antofagasta" : ["Antofagasta", "Mejillones", "Sierra Gorda", "Taltal", "Calama", "Ollagüe", "San Pedro de Atacama", "María Elena", "Tocopilla"],
    "Atacama" : ["Chañaral", "Diego de Almagro", "Caldera", "Copiapó", "Tierra Amarilla", "Alto del Carmen", "Freirina", "Huasco", "Vallenar"],
    "Coquimbo" : ["Canela", "Illapel", "Los Vilos", "Salamanca", "Andacollo", "Coquimbo", "La Higuera", "La Serena", "Paihuano", "Vicuña", "Combarbalá", "Monte Patria", "Ovalle", "Punitaqui", "Río Hurtado"],
    "Valparaíso" : ["Isla de Pascua", "Calle Larga", "Los Andes", "Rinconada de los Andes", "San Esteban", "Limache", "Olmué", "Quilpué", "Villa Alemana", "Cabildo", "La Ligua", "Papudo", "Petorca", "Zapallar", "Hijuelas", "La Calera", "La Cruz", "Nogales", "Quillota", "Algarrobo", "Cartagena", "El Quisco", "El Tabo", "San Antonio", "Santo Domingo", "Catemu", "Llaillay", "Panquehue", "Putaendo", "San Felipe", "Santa María", "Casablanca", "Concón", "Juan Fernández", "Puchuncaví", "Quintero", "Valparaíso", "Viña del Mar"],
    "Región del Libertador Gral. Bernardo O’Higgins" : ["Codegua", "Coinco", "Coltauco", "Doñihue", "Graneros", "Las Cabras", "Machalí", "Malloa", "Olivar", "Peumo", "Pichidegua", "Quinta de Tilcoco", "Rancagua", "Requínoa", "Rengo", "San Francisco de Mostazal", "San Vicente de Tagua Tagua", "La Estrella", "Litueche", "Marchigüe", "Navidad", "Paredones", "Pichilemu", "Chépica", "Chimbarongo", "Lolol", "Nancagua", "Palmilla", "Peralillo", "Placilla", "Pumanque", "San Fernando", "Santa Cruz"],
    "Región del Maule" : ["Cauquenes", "Chanco", "Pelluhue", "Curicó", "Hualañé", "Licantén", "Molina", "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén", "Colbún", "Linares", "Longaví", "Parral", "Retiro", "San Javier de Loncomilla", "Villa Alegre", "Yerbas Buenas", "Constitución", "Curepto", "Empedrado", "Maule", "Pelarco", "Pencahue", "Río Claro", "San Clemente", "San Rafael", "Talca"],
    "Ñuble" : ["Bulnes", "Chillán", "Chillán Viejo", "El Carmen", "Pemuco", "Pinto", "Quillón", "San Ignacio", "Yungay", "Cobquecura", "Coelemu", "Ninhue", "Portezuelo", "Quirihue", "Ránquil", "Treguaco", "Coihueco", "Ñiquén", "San Carlos", "San Fabián", "San Nicolás"],
    "Región del Biobío" : ["Arauco", "Cañete", "Contulmo", "Curanilahue", "Lebu", "Los Álamos", "Tirúa", "Alto Biobío", "Antuco", "Cabrero", "Laja", "Los Ángeles", "Mulchén", "Nacimiento", "Negrete", "Quilaco", "Quilleco", "San Rosendo", "Santa Bárbara", "Tucapel", "Yumbel", "Chiguayante", "Concepción", "Coronel", "Florida", "Hualpén", "Hualqui", "Lota", "Penco", "San Pedro de la Paz", "Santa Juana", "Talcahuano", "Tomé"],
    "Región de la Araucanía" : ["Carahue", "Cholchol", "Cunco", "Curarrehue", "Freire", "Galvarino", "Gorbea", "Lautaro", "Loncoche", "Melipeuco", "Nueva Imperial", "Padre Las Casas", "Perquenco", "Pitrufquén", "Pucón", "Saavedra", "Temuco", "Teodoro Schmidt", "Toltén", "Vilcún", "Villarrica", "Angol", "Collipulli", "Curacautín", "Ercilla", "Lonquimay", "Los Sauces", "Lumaco", "Purén", "Renaico", "Traiguén", "Victoria"],
    "Región de Los Ríos" : ["Futrono", "La Unión", "Lago Ranco", "Río Bueno", "Corral", "Lanco", "Los Lagos", "Máfil", "Mariquina", "Paillaco", "Panguipulli", "Valdivia"],
    "Región de Los Lagos" : [ "Ancud", "Castro", "Chonchi", "Curaco de Vélez", "Dalcahue", "Puqueldón", "Queilén", "Quellón", "Quemchi", "Quinchao", "Calbuco", "Cochamó", "Fresia", "Frutillar", "Llanquihue", "Los Muermos", "Maullín", "Puerto Montt", "Puerto Varas", "Osorno", "Puerto Octay", "Purranque", "Puyehue", "Río Negro", "San Pablo", "San Juan de la Costa", "Chaitén", "Futaleufú", "Hualaihué", "Palena"],
    "Región Aisén del Gral. Carlos Ibáñez del Campo" : ["Aysén", "Cisnes", "Guaitecas", "Cochrane", "O'Higgins", "Tortel", "Coyhaique", "Lago Verde", "Chile Chico", "Río Ibáñez"],
    "Región de Magallanes y de la Antártica Chilena" : ["Antártica", "Cabo de Hornos", "Laguna Blanca", "Punta Arenas", "Río Verde", "San Gregorio", "Porvenir", "Primavera", "Timaukel", "Natales", "Torres del Paine"],
    "Región Metropolitana de Santiago" : ["Colina", "Lampa", "Tiltil", "Pirque", "Puente Alto", "San José de Maipo", "Buin", "Calera de Tango", "Paine", "San Bernardo", "Alhué", "Curacaví", "María Pinto", "Melipilla", "San Pedro", "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central", "Huechuraba", "Independencia", "La Cisterna", "La Granja", "La Florida", "La Pintana", "La Reina", "Las Condes", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú", "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén", "Providencia", "Pudahuel", "Quilicura", "Quinta Normal", "Recoleta", "Renca", "San Miguel", "San Joaquín", "San Ramón", "Santiago", "Vitacura", "El Monte", "Isla de Maipo", "Padre Hurtado", "Peñaflor", "Talagante"]
}


/*
* Genera las opciones de las regiones para el dropdown del formulario.
*/
function make_regiones() {
    node = document.getElementById("region");
    html_inject = '<option value=""> Seleccione una región </option>';
    for (value of Object.keys(comunas)){
        html_inject += `
        <option value="${value}">${value}</option>`;
    };
    node.innerHTML = html_inject;
}


/**
 * Se ejecuta cuando se cambia la región en el formulario, actualiza el dropdown de comunas
 * con las que pertenecen a la nueva región
 * @param {dropdown regiones} node
 */
function region_change(node) {
    comunas_node = document.getElementById("comuna");
    options = '<option value=""> Seleccione una Comuna </option>';
    region_actual = node.value;
    if (region_actual != "") {
        for (comuna of comunas[region_actual]) {
            options += `<option value="${comuna}">${comuna}</option>`;
        }
    }
    comunas_node.innerHTML = options;
}