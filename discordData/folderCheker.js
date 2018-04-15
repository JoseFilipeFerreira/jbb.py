var id = require('./channelID.json');

function admintools(channelID){
	return (id.botTester      == channelID ||
		    id.newQuotes      == channelID ||
		    id.salaDeReuniões == channelID ||
		    id.adminCesium    == channelID);
}

function escolheatuacor(channelID){
	return (escolheatuacor == channelID);
}

function geral(channelID){
    return(id.geral         == channelID ||
    	   id.regras        == channelID ||
    	   id.avisos        == channelID ||
    	   id.sugestões     == channelID ||
    	   id.dankMemes     == channelID ||
    	   id.discospedidos == channelID ||
    	   id.gaming        == channelID);
}

function geralnotimportant(channelID){
    return(id.geral         == channelID ||
    	   id.dankMemes     == channelID ||
    	   id.discospedidos == channelID ||
    	   id.gaming        == channelID);
}

function cesium(channelID){
	return(id.cesiumDiscussão  == channelID ||
		   id.cesiumDivulgação == channelID);
}

function análise(channelID){
    return(id.avisosA    == channelID ||
           id.dúvidasA   == channelID ||
           id.ficheirosA == channelID ||
           id.imagensA   == channelID);
}

function lógica(channelID){
	return(id.avisosL    == channelID ||
           id.dúvidasL   == channelID ||
           id.ficheirosL == channelID ||
           id.imagensL   == channelID);
}

function programação(channelID){
	return(id.avisosPF    == channelID ||
           id.dúvidasPF   == channelID ||
           id.ficheirosPF == channelID ||
           id.imagensPF   == channelID);
}

function sistemas(channelID){
	return(id.avisosSC    == channelID ||
           id.dúvidasSC   == channelID ||
           id.ficheirosSC == channelID ||
           id.imagensSC   == channelID);
}

function laboratórios(channelID){
	return(id.avisosLI    == channelID ||
           id.dúvidasLI   == channelID ||
           id.ficheirosLI == channelID ||
           id.imagensLI   == channelID);
}

function tópicos(channelID){
	return(id.avisosTFM    == channelID ||
           id.dúvidasTFM   == channelID ||
           id.ficheirosTFM == channelID ||
           id.imagensTFM   == channelID);
}

module.exports = {
    admintools:admintools,
    escolheatuacor:escolheatuacor,
    geral:geral,
    geralnotimportant:geralnotimportant,
    cesium:cesium,
    análise:análise,
    lógica:lógica,
    programação:programação,
    sistemas:sistemas,
    laboratórios:laboratórios,
    tópicos:tópicos
}
